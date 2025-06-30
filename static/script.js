function clickOnEnter(input, btn) {
    input.addEventListener("keydown", event => {
        if (event.key == "Enter") {
            btn.click();
        }
    })
}

function renderTable(data) {
    const table = document.createElement('table');

    // Table headers
    table.innerHTML = `
        <thead>
        <tr>
            <th>Company</th>
            <th>Fit Criteria</th>
            <th>Keyword Found</th>
            <th>Followers</th>
            <th>Employees</th>
        </tr>
        </thead>
        <tbody>
        ${Object.entries(data).map(([company, info]) => {
            const hasError = info.Error !== null;
            const row = `
            <tr>
                <td>
                ${company}
                ${hasError ? `<div class="error-msg">${info.Error}</div>` : ''}
                </td>
                <td>${hasError ? '❌' : info.Passed ? '✅' : '❌'}</td>
                <td>${hasError ? '❌' : info["Keyword found"] ? '✅' : '❌'}</td>
                <td>${hasError ? '❌' : info.Followers ? '✅' : '❌'}</td>
                <td>${hasError ? '❌' : info.Employees ? '✅' : '❌'}</td>
            </tr>
            `;
            return row;
        }).join('')}
        </tbody>
    `;

    resultsTable.appendChild(table);
    resultsTable.scrollIntoView()
}

let searchBtn = document.querySelector("#search");
let spinner = document.getElementById("spinner");
let resultsTable = document.getElementById("results-table");
searchBtn.addEventListener("click", async () => {
    let errorMsg = document.querySelector(".error");

    let allCompanies = document.querySelectorAll("#company");
    let companies = [];
    for (const company of allCompanies) {
        let name = company.textContent.slice(0,-1);
        companies.push(name)
    }

    let allKeywords = document.querySelectorAll("#keyword");
    let keywords = [];
    for (const keyword of allKeywords) {
        let kw = keyword.textContent.slice(0, -1);
        keywords.push(kw);
    }
    
    let minFollowers = document.getElementById("min-followers").value;
    let maxFollowers = document.getElementById("max-followers").value;

    let minEmployees = document.getElementById("min-employees").value;
    let maxEmployees = document.getElementById("max-employees").value;

    if ((keywords.length == 0) && (minFollowers == "") && (maxFollowers == "") && (minEmployees == "") && (maxEmployees == "")) {
        errorMsg.hidden = false;
        errorMsg.textContent = "No criteria set."
        return;
    } else if (companies.length == 0) {
        errorMsg.hidden = false;
        errorMsg.textContent = "No companies added."
        return
    }

    errorMsg.hidden = true

    spinner.style.display = 'block';
    resultsTable.innerHTML = '';
    spinner.scrollIntoView();
    
    let response = await fetch("/load", {
        method: "POST",
        headers:{
                'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "companies": companies,
            "keywords": keywords,
            "min_followers": minFollowers,
            "max_followers": maxFollowers,
            "min_employees": minEmployees,
            "max_employees": maxEmployees
        })
    });
    
    let data = await response.json();
    renderTable(data);

    spinner.style.display = "none";

})

let addKwBtn = document.getElementById("add-keyword");
let addKwInput = document.getElementById("add-keywords");
clickOnEnter(addKwInput, addKwBtn);

addKwBtn.addEventListener("click", () => {
    let keyword = addKwInput.value.trim();

    if (keyword === "") {
        return;
    }

    let container = document.getElementById("keywords-container");
    let newKw = document.createElement("div");
    newKw.id = "keyword";
    newKw.classList.add("keyword-box", "tag-box");
    newKw.textContent = keyword.toLowerCase();
    let kwDel = document.createElement("span")
    kwDel.textContent = "x";
    kwDel.id = "delete-keyword";
    kwDel.classList.add("remove-btn");

    newKw.appendChild(kwDel);

    container.appendChild(newKw);

    kwDel.addEventListener("click", () => {
        container.removeChild(newKw);
    })

    addKwInput.value = "";
})

let addCompBtn = document.getElementById("add-company");
let addCompInput = document.getElementById("add-companies");
clickOnEnter(addCompInput, addCompBtn);

addCompBtn.addEventListener("click", () => {
    let company = addCompInput.value.trim();

    if (company === "") {
        return;
    }

    let container = document.getElementById("companies-container");
    let addContainer = document.getElementById("add-company-container");
    let newComp = document.createElement("div");
    newComp.id = "company";
    newComp.textContent = company;
    newComp.classList.add("company-item");
    let compDel = document.createElement("span")
    compDel.textContent = "x";
    compDel.id = "delete-company";
    compDel.classList.add("remove-btn")

    newComp.appendChild(compDel);

    container.insertBefore(newComp, addContainer);

    compDel.addEventListener("click", () => {
        container.removeChild(newComp);
        let allCompanies = document.querySelectorAll("#company");
        if (allCompanies.length < 5) {
            addContainer.querySelector("#limit").hidden = true;
            addCompBtn.hidden = false;
            addCompInput.hidden = false;
        }
    })

    addCompInput.value = "";

    let allCompanies = document.querySelectorAll("#company");
    if (allCompanies.length >= 5) {
        addContainer.querySelector("#limit").hidden = false;
        addCompBtn.hidden = true;
        addCompInput.hidden = true;
    }
})