import { setupSourceSelect, formatISODate } from "./utils.js";

const searchButton = document.getElementById("search-btn");
const articleContainer = document.getElementById("article-list");

const sourceSelect = document.getElementById("source");
setupSourceSelect(sourceSelect);

function displayArticles(articles) {
    articleContainer.innerHTML = "";

    const content = articles.map((article) =>
        `<div class='article'>
            <a href=${article["loc"]}>${article["title"]}</a>
            <div class="meta">${article["origin"]} - ${formatISODate(article["publication_date"])}</div>
        </div>`
    ).join("");

    articleContainer.innerHTML = content;
}

searchButton.addEventListener("click", async () => {
    const source = document.getElementById("source").value.trim();
    const dateStart = document.getElementById("date-start").value;
    const dateEnd = document.getElementById("date-end").value;
    const keywords = document.getElementById("keywords").value.trim().split(" ");

    const response = await fetch(`/api/articles?origin=${source}&date_start=${dateStart}&date_end=${dateEnd}&keywords=${keywords.join(",")}`);
    const articles = await response.json();

    displayArticles(articles);
});