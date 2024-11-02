function createTable(columns, data) {
    // Create result count
    const resultCount = document.createElement('div');
    resultCount.className = 'result-count';
    resultCount.textContent = `Found ${data.length} result${data.length !== 1 ? 's' : ''}`;
    
    // Create table element
    const table = document.createElement('table');
    
    // Create header row
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column.toUpperCase().replace('_', ' ');
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement('tbody');
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(column => {
            const td = document.createElement('td');
            td.textContent = row[column] || '';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    
    // Create container for count and table
    const container = document.createElement('div');
    container.appendChild(resultCount);
    container.appendChild(table);
    
    return container;
}

document.getElementById('lookup-form').onsubmit = async (e) => {
    e.preventDefault();
    const postcode = document.getElementById('postcode').value;
    const resultDiv = document.getElementById('result');
    
    try {
        const response = await fetch('/lookup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `postcode=${encodeURIComponent(postcode)}`
        });
        
        const data = await response.json();
        resultDiv.style.display = 'block';
        
        if (response.ok) {
            resultDiv.className = 'result success';
            resultDiv.innerHTML = ''; // Clear previous results
            const tableContainer = createTable(data.columns, data.data);
            resultDiv.appendChild(tableContainer);
        } else {
            resultDiv.className = 'result error';
            resultDiv.textContent = data.error;
        }
    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'result error';
        resultDiv.textContent = 'An error occurred. Please try again.';
    }
};