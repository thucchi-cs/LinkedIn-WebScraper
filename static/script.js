function clickOnEnter(input, btn) {
    input.addEventListener("keydown", event => {
        if (event.key == "Enter") {
            btn.click();
        }
    })
}

let searchBtn = document.querySelector("#search");
searchBtn.addEventListener("click", async () => {
    document.getElementById("wait").hidden = false;

    let allCompanies = document.querySelectorAll("#company");
    let companies = [];
    for (const company of allCompanies) {
        let name = company.querySelector("span").textContent;
        companies.push(name)
    }

    let allKeywords = document.querySelectorAll("#keyword");
    let keywords = [];
    for (const keyword of allKeywords) {
        let kw = keyword.querySelector("span").textContent;
        keywords.push(kw);
    }

    let minFollowers = document.getElementById("min-followers").value;
    let maxFollowers = document.getElementById("max-followers").value;

    let minEmployees = document.getElementById("min-employees").value;
    let maxEmployees = document.getElementById("max-employees").value;

    if ((keywords.length == 0) && (minFollowers == "") && (maxFollowers == "") && (minEmployees == "") && (maxEmployees == "")) {
        console.log("no criteria :(");
        return;
    } else if (companies.length == 0) {
        console.log("no companies :((");
        return
    }
    
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
    
    let data = await response.text();

    document.getElementById("wait").hidden = true;

    let dataDiv = document.getElementById("data");
    dataDiv.hidden = false;
    dataDiv.innerHTML = data;
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
    let kwTxt = document.createElement("span");
    kwTxt.textContent = keyword.toLowerCase();
    let kwDel = document.createElement("button")
    kwDel.type = "button";
    kwDel.textContent = "-";
    kwDel.id = "delete-keyword";

    newKw.appendChild(kwTxt);
    newKw.appendChild(kwDel);

    container.insertBefore(newKw, addKwInput);

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
    let compTxt = document.createElement("span");
    compTxt.textContent = company;
    let compDel = document.createElement("button")
    compDel.type = "button";
    compDel.textContent = "x";
    compDel.id = "delete-company";

    newComp.appendChild(compTxt);
    newComp.appendChild(compDel);

    container.insertBefore(newComp, addContainer);

    compDel.addEventListener("click", () => {
        container.removeChild(newComp);
        let allCompanies = document.querySelectorAll("#company");
        if (allCompanies.length < 5) {
            addContainer.hidden = false;
        }
    })

    addCompInput.value = "";

    let allCompanies = document.querySelectorAll("#company");
    if (allCompanies.length >= 5) {
        addContainer.hidden = true;
    }
})