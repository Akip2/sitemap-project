import { formatTimestamp } from "./utils.js";

const addSourceButton = document.getElementById("add-source-btn");
const sourceContainer = document.getElementById("source-list");
sourceContainer.addEventListener("click", (e) => {
    const target = e.target;
    if (target.classList.contains("delete-btn")) {
        deleteSource(target.id);
    }
});

async function deleteSource(sourceName) {
    const response = await fetch(`/api/sources/${sourceName}`, {
        method: "DELETE"
    });

    if (response.status === 200) {
        updateSourceContainer();
    }
}

async function updateSourceContainer() {
    const response = await fetch("/api/sources");
    const sources = await response.json();

    let content
    if (sources.length > 0) {
        content = sources.map((source) =>
            `
        <div class='source'>
            <div>
                <a href=${source.url}>${source.name}</a>
                <div class="meta"><b>Dernière update</b>: ${formatTimestamp(source.last_update)}</div>
                <div class="meta"><b>Prochaine update</b>: ${formatTimestamp(source.last_update + source.time_interval)}</div>
            </div>
            <button class="delete-btn" id="${source.name}">Se désabonner</button>
        </div>
        `).join("");
    } else {
        content = "<p>Aucun abonnement</p>";
    }

    sourceContainer.innerHTML = content;
}

addSourceButton.addEventListener("click", async () => {
    const url = document.getElementById("url").value.trim();
    const interval = document.getElementById("interval").value.trim();
    const timeUnit = document.getElementById("unit").value;

    if (url.length === 0 || interval.length === 0) {
        alert("Veuillez remplir tous les champs");
        return;
    } else if (isNaN(interval) || parseInt(interval) <= 0) {
        alert("L'intervalle doit être un nombre entier positif");
        return;
    }

    let timeCoef;
    switch (timeUnit) {
        case "minutes":
            timeCoef = 60;
            break;
        case "hours":
            timeCoef = 3600;
            break;
        case "days":
            timeCoef = 86400;
            break;
    }

    const response = await fetch("/api/sources", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "url": url,
            "time_interval": parseInt(interval) * timeCoef
        })
    });

    if (response.status === 200) {
        updateSourceContainer();
    }
});

updateSourceContainer()