function searchBooks() {
    const form = document.getElementById('search-form');
    const formData = new FormData(form);
    const queryParams = new URLSearchParams(formData).toString();

    fetch(`/live-search/?${queryParams}`)
        .then(response => response.json())
        .then(data => {
            const booksList = document.getElementById('books-list');
            booksList.innerHTML = '';

            if (data.books.length === 0) {
                booksList.innerHTML = '<tr><td colspan="6" class="text-center">No books found</td></tr>';
            } else {
                data.books.forEach(book => {
                    booksList.innerHTML += `
                        <tr>
                            <td>${book.book_code}</td>
                            <td>${book.name}</td>
                            <td>${book.authors}</td>
                            <td>${book.year}</td>
                            <td>${book.book_lang}</td>
                            <td>${book.number}</td>
                        </tr>
                    `;
                });
            }
        });
}
