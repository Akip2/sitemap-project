export function formatTimestamp(ts) {
    const date = new Date(ts * 1000);

    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);

    return `${hours}:${minutes} ${day}/${month}/${year}`;
}

export async function setupSourceSelect(select) {
    const response = await fetch("/api/sources");
    const sources = await response.json();

    const options = sources.map((source) =>
        `<option value="${source.name}">${source.name}</option>`
    ).join("");

    const defaultOption = "<option value='' selected>Toutes</option>";

    select.innerHTML = defaultOption + options;
}