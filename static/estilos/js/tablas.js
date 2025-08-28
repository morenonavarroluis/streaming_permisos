  document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('myTable');
    const tbody = table.querySelector('tbody');
    const searchInput = document.getElementById('searchInput');
    const rowsPerPageSelect = document.getElementById('rowsPerPage');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageNumbersSpan = document.getElementById('pageNumbers');

    // Get all original rows from the table body
    const allRows = Array.from(tbody.querySelectorAll('tr'));
    let filteredRows = [...allRows]; // Rows currently matching the search filter
    let currentPage = 1;
    let rowsPerPage = parseInt(rowsPerPageSelect.value);

    // --- Functions ---

    // Renders the table based on current filteredRows, currentPage, and rowsPerPage
    function renderTable() {
        tbody.innerHTML = ''; // Clear current table content

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const paginatedRows = filteredRows.slice(start, end);

        if (paginatedRows.length === 0) {
            const noResultsRow = document.createElement('tr');
            noResultsRow.innerHTML = `<td colspan="${table.querySelectorAll('th').length}" style="text-align: center; padding: 20px;">No se encontraron resultados.</td>`;
            tbody.appendChild(noResultsRow);
        } else {
            paginatedRows.forEach(row => tbody.appendChild(row));
        }

        updatePaginationControls();
    }

    // Updates the page numbers and button states
    function updatePaginationControls() {
        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        pageNumbersSpan.textContent = `Página ${currentPage} de ${totalPages}`;

        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages || totalPages === 0;
    }

    // Handles search input
    function handleSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();

        if (searchTerm === '') {
            filteredRows = [...allRows]; // If search is empty, show all rows
        } else {
            filteredRows = allRows.filter(row => {
                // Check if any cell in the row contains the search term
                return Array.from(row.children).some(cell =>
                    cell.textContent.toLowerCase().includes(searchTerm)
                );
            });
        }
        currentPage = 1; // Reset to first page after search
        renderTable();
    }

    // Handles rows per page change
    function handleRowsPerPageChange() {
        rowsPerPage = parseInt(rowsPerPageSelect.value);
        currentPage = 1; // Reset to first page
        renderTable();
    }

    // Handles previous page button click
    function handlePrevClick() {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    }

    // Handles next page button click
    function handleNextClick() {
        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    }

    // --- Event Listeners ---
    searchInput.addEventListener('input', handleSearch);
    rowsPerPageSelect.addEventListener('change', handleRowsPerPageChange);
    prevBtn.addEventListener('click', handlePrevClick);
    nextBtn.addEventListener('click', handleNextClick);

    // Initial render when the page loads
    renderTable();
});