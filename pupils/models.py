from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from django.utils.text import slugify
import cv2
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import numpy as np


def user_face_path(instance, filename):
    first_name = slugify(instance.first_name)
    last_name = slugify(instance.last_name)
    filename_base, filename_ext = os.path.splitext(filename)
    new_filename = f"{first_name}_{last_name}{filename_ext}"
    return f"user_faces/{new_filename}"


class Pupil(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    group = models.CharField(max_length=15, null=False, blank=False)
    course = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ],
        null=True,
        blank=True
    )
    books = models.JSONField(blank=True, default=list)
    face_image = models.ImageField(upload_to=user_face_path)
    face_encoding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        if self.face_image:
            if os.path.isfile(self.face_image.path):
                os.remove(self.face_image.path)
        super().delete(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.face_image and not self.pk:  # Faqat yangi yaratilayotgan objectlar uchun
            self.check_duplicate_face()

    def check_duplicate_face(self):
        try:
            # Joriy rasmni o'qib olamiz
            img_path = self.face_image.path
            image = cv2.imread(img_path)

            if image is None:
                return

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            if len(faces) == 0:
                return

            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (100, 100))
            current_encoding = face_roi.tobytes()

            # Bazadagi barcha talabalarni tekshiramiz
            for pupil in Pupil.objects.exclude(pk=self.pk):
                if pupil.face_encoding:
                    stored_encoding = np.frombuffer(pupil.face_encoding, dtype=np.uint8)
                    stored_encoding = stored_encoding.reshape(100, 100)

                    difference = cv2.absdiff(stored_encoding, face_roi)
                    similarity = 1 - (np.sum(difference) / (100 * 100 * 255))

                    if similarity > 0.5:  # 80% o'xshashlik
                        raise ValidationError(
                            {'face_image': 'Bu yuz allaqachon bazada mavjud. Foydalanuvchi: %s %s' % (
                                pupil.first_name, pupil.last_name
                            )}
                        )
        except Exception as e:
            print(f"Yuzni solishtirishda xato: {e}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.face_image and not self.face_encoding:
            try:
                img_path = self.face_image.path
                image = cv2.imread(img_path)

                if image is not None:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

                    if len(faces) > 0:
                        (x, y, w, h) = faces[0]
                        face_roi = gray[y:y + h, x:x + w]
                        face_roi = cv2.resize(face_roi, (100, 100))
                        self.face_encoding = face_roi.tobytes()
                        super().save(update_fields=['face_encoding'])
            except Exception as e:
                print(f"Yuz kodlashda xato: {e}")


@receiver(pre_delete, sender=Pupil)
def delete_pupil_files(sender, instance, **kwargs):
    """
    Talaba o'chirilishidan oldin unga tegishli fayllarni o'chiradi
    """
    if instance.face_image:
        if os.path.isfile(instance.face_image.path):
            os.remove(instance.face_image.path)
        # Papkani ham o'chirish (agar bo'sh bo'lsa)
        folder_path = os.path.dirname(instance.face_image.path)
        if os.path.exists(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)