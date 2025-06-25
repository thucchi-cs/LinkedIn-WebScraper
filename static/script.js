let btn = document.querySelector("button");
btn.addEventListener("click", async () => {
    document.getElementById("wait").hidden = false;

    let company = document.getElementById("company").value.toLowerCase();
    company = company.trim().replace(" ", "-");
    let url = `https://www.linkedin.com/company/${company}`;
    
    let response = await fetch("/load", {
        method: "POST",
        headers:{
                'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "url": url
        })
    });
    let data = await response.text();

    document.getElementById("wait").hidden = true;

    let dataDiv = document.getElementById("data");
    dataDiv.hidden = false;
    dataDiv.innerHTML = data;
})