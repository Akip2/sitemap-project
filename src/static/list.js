import { displayArticles } from "./utils.js";

const searchButton = document.getElementById("search-btn");

searchButton.addEventListener("click", async () => {
    const source = document.getElementById("source").value.trim();
    const dateStart = document.getElementById("date-start").value;
    const dateEnd = document.getElementById("date-end").value;
    const keywords = document.getElementById("keywords").value.trim().split(" ");

    const response = await fetch("/api/articles");
    const articles = await response.json();

    displayArticles(articles);
});