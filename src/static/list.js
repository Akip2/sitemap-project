import { setupSourceSelect, formatISODate, formatTimestamp } from "./utils.js";

const searchButton = document.getElementById("search-btn");
const articleContainer = document.getElementById("article-list");

const sourceSelect = document.getElementById("source");
setupSourceSelect(sourceSelect);

function recordConsultation(loc) {
    const timestamp = Date.now() / 1000;
    fetch('/api/consultations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ loc: loc, timestamp: timestamp }),
    });
}

function displayArticles(articles) {
    articleContainer.innerHTML = "";

    const content = articles.map((article) =>
        `<div class='article'>
            <a href=${article["loc"]} target="_blank">${article["title"]}</a>
            ${article["image_loc"] ? `<img src="${article["image_loc"]}"/>` : ""}
            <div class="meta"><p>${article["origin"]} - ${formatISODate(article["publication_date"])}</p>` +
            `${article["last_consultation"] ? `<p>Dernière consultation: ${formatTimestamp(article["last_consultation"])}</p>` : ""}</div>
        </div>`
    ).join("");

    articleContainer.innerHTML = content;

    const links = articleContainer.querySelectorAll('.article a');
    links.forEach(link => {
        link.addEventListener('click', () => recordConsultation(link.href));
    });
}

searchButton.addEventListener("click", async () => {
    const source = document.getElementById("source").value.trim();
    const dateStart = document.getElementById("date-start").value;
    const dateEnd = document.getElementById("date-end").value;
    const consultationDate = document.getElementById("consultation-date").value;
    const consultationTime = document.getElementById("consultation-time").value;
    const keywords = document.getElementById("keywords").value.trim().split(" ");

    const response = await fetch(`/api/articles?origin=${source}&date_start=${dateStart}&date_end=${dateEnd}&consultation_date=${consultationDate}&consultation_time=${consultationTime}&keywords=${keywords.join(",")}`);
    const articles = await response.json();

    displayArticles(articles);
});