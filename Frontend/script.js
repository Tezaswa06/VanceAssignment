const form = document.getElementById("forexForm");
const resultDiv = document.getElementById("resultList");
const loadingIndicator = document.getElementById("loading");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Clear previous results
  resultDiv.innerHTML = "";
  loadingIndicator.style.display = "block"; // Show loading indicator

  const fromCurrency = document.getElementById("from").value.toUpperCase();
  const toCurrency = document.getElementById("to").value.toUpperCase();
  const period = document.getElementById("period").value;

  if (!fromCurrency || !toCurrency || !period) {
    loadingIndicator.style.display = "none"; // Hide loading indicator
    resultDiv.innerHTML = `<p class="error">Please fill all fields.</p>`;
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/api/forex-data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ from: fromCurrency, to: toCurrency, period: period }),
    });

    loadingIndicator.style.display = "none"; // Hide loading indicator

    if (response.ok) {
      const data = await response.json();
      displayResults(data);
    } else {
      const error = await response.json();
      resultDiv.innerHTML = `<p class="error">${error.message || "Error fetching data"}</p>`;
    }
  } catch (err) {
    console.error(err);
    loadingIndicator.style.display = "none"; // Hide loading indicator
    resultDiv.innerHTML = `<p class="error">An error occurred while fetching data.</p>`;
  }
});

function displayResults(data) {
  if (!data || data.length === 0) {
    resultDiv.innerHTML = `<p>No data available for the given period.</p>`;
    return;
  }

  const table = document.createElement("table");
  table.className = "forex-table";

  // Create table header
  const headerRow = document.createElement("tr");
  const headers = ["Date", "Open", "High", "Low", "Close", "Volume"];
  headers.forEach((header) => {
    const th = document.createElement("th");
    th.textContent = header;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  // Populate table rows
  data.forEach((entry) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${entry.date}</td>
      <td>${entry.open}</td>
      <td>${entry.high}</td>
      <td>${entry.low}</td>
      <td>${entry.close}</td>
      <td>${entry.volume}</td>
    `;
    table.appendChild(row);
  });

  resultDiv.appendChild(table);
}
