const addSourceButton = document.getElementById("add-source-btn");
const sourceContainer = document.getElementById("source-list");

async function updateSourceContainer() {
    const response = await fetch("/api/sources");
    const sources = await response.json();

    const content = sources.map((source) => `<div><a href=${source.url}>${source.name}</a>`).join("");
    sourceContainer.innerHTML = content;
}

addSourceButton.addEventListener("click", async () => {
    const url = document.getElementById("url").value.trim();

    const response = await fetch("/api/sources", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "url": url
        })
    });

    if(response.status === 200) {
        updateSourceContainer();
    }
});

updateSourceContainer()