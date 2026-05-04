const articleContainer = document.getElementById("article-list");

export function displayArticles(articles) {
    articleContainer.innerHTML = "";

    const content = articles.map((article) =>
        `<div class='article'>
            <a href=${article["loc"]}>${article["title"]}</a>
        </div>`
        ).join("");
    
    console.log(content);

    articleContainer.innerHTML = content;
}