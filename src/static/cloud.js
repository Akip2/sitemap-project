import { setupSourceSelect } from "./utils.js";

const WIDTH = 800;
const HEIGHT = 400;
const COLORS = ["#0013ff", "#0066ff", "#07a5df"];

const sourceSelect = document.getElementById("source");
setupSourceSelect(sourceSelect);

document.getElementById("gen-btn").addEventListener("click", async () => {
    const source = document.getElementById("source").value.trim();
    const dateStart = document.getElementById("date-start").value;
    const dateEnd = document.getElementById("date-end").value;
    const nbWord = parseInt(document.getElementById("nb-word").value);

    if (isNaN(nbWord) || nbWord <= 0) {
        alert("Le nombre de mots doit être un nombre entier positif");
        return;
    }

    const response = await fetch(`/api/wordcloud?origin=${source}&date_start=${dateStart}&date_end=${dateEnd}&nb_word=${nbWord}`);
    const words = await response.json();
    displayWordCloud(words);
});

function getFontSize(freq, minFreq, maxFreq) {
    return 10 + ((freq - minFreq) / (maxFreq - minFreq + 1)) * 40;
}

function placeRing(ringWords, radius, minFreq, maxFreq) {
    const n = ringWords.length;
    const angleOffset = Math.PI / 6;

    return ringWords.map(([word, freq], i) => {
        const size = getFontSize(freq, minFreq, maxFreq);
        const color = COLORS[Math.floor(Math.random() * COLORS.length)];
        const angle = angleOffset + (2 * Math.PI / n) * i;
        const x = WIDTH / 2 + radius * Math.cos(angle);
        const y = HEIGHT / 2 + radius * Math.sin(angle) * 0.5;
        return `<text x="${x}" y="${y}" font-size="${size}" fill="${color}"
            text-anchor="middle" dominant-baseline="middle">${word}</text>`;
    });
}

function displayWordCloud(words) {
    const maxFreq = words[0][1];
    const minFreq = words[words.length - 1][1];
    const elements = [];

    let radius = 0;
    let ringWords = [words[0]];
    let remaining = words.slice(1);

    while (ringWords.length > 0) {
        elements.push(...placeRing(ringWords, radius, minFreq, maxFreq));

        const avgSize = getFontSize(ringWords[0][1], minFreq, maxFreq);
        const nextRadius = radius + avgSize * 2;
        const capacity = Math.max(1, Math.floor(2 * Math.PI * nextRadius / (avgSize * 3)));

        radius = nextRadius;
        ringWords = remaining.slice(0, capacity);
        remaining = remaining.slice(capacity);
    }

    document.getElementById("cloud").innerHTML =
        `<svg width="${WIDTH}" height="${HEIGHT}">${elements.join("")}</svg>`;
}