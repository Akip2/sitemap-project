const addSourceButton = document.getElementById("add-source-btn");

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
});
