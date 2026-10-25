const groups = {
  "Base surfaces": ["background", "foreground", "cursorColor", "selectionBackground"],
  "Normal ANSI": ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"],
  "Bright ANSI": ["brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite"],
};

const labels = {
  cursorColor: "Cursor", selectionBackground: "Selection",
  brightBlack: "Bright black", brightRed: "Bright red", brightGreen: "Bright green",
  brightYellow: "Bright yellow", brightBlue: "Bright blue", brightPurple: "Bright purple",
  brightCyan: "Bright cyan", brightWhite: "Bright white",
};

let original;
let theme;

const title = key => labels[key] || key[0].toUpperCase() + key.slice(1);
const validHex = value => /^#[0-9a-f]{6}$/i.test(value);

function relativeLuminance(hex) {
  const channels = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map(c => c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4);
  return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2];
}

function contrast(a, b) {
  const [light, dark] = [relativeLuminance(a), relativeLuminance(b)].sort((x, y) => y - x);
  return (light + .05) / (dark + .05);
}

function renderControls() {
  const root = document.querySelector("#color-controls");
  root.innerHTML = "";
  Object.entries(groups).forEach(([groupName, keys]) => {
    const group = document.createElement("section");
    group.className = "control-group";
    group.innerHTML = `<h3>${groupName}</h3>`;
    keys.forEach(key => {
      const row = document.createElement("div");
      row.className = "color-control";
      row.innerHTML = `<input type="color" value="${theme[key]}" aria-label="Pick ${title(key)} color" title="Open ${title(key)} color picker"><label>${title(key)}</label><input type="text" value="${theme[key]}" aria-label="${title(key)} hex">`;
      const [picker, , text] = row.children;
      picker.addEventListener("input", () => updateColor(key, picker.value));
      text.addEventListener("change", () => {
        if (validHex(text.value)) updateColor(key, text.value);
        else text.value = theme[key];
      });
      row.dataset.key = key;
      group.appendChild(row);
    });
    root.appendChild(group);
  });
}

function updateColor(key, value) {
  theme[key] = value.toUpperCase();
  const row = document.querySelector(`.color-control[data-key="${key}"]`);
  row.querySelector('input[type="color"]').value = value;
  row.querySelector('input[type="text"]').value = theme[key];
  renderPreview();
  document.querySelector("#status").textContent = "Unsaved changes";
}

function renderPreview() {
  document.querySelector("#terminal-preview").style.background = theme.background;
  document.querySelector(".terminal-body").style.color = theme.foreground;
  document.querySelector(".selection").style.background = theme.selectionBackground;
  document.querySelector(".cursor").style.background = theme.cursorColor;
  document.querySelectorAll("[data-color]").forEach(node => node.style.color = theme[node.dataset.color]);

  const ansi = [...groups["Normal ANSI"], ...groups["Bright ANSI"]];
  document.querySelector("#swatches").innerHTML = ansi.map(key => `
    <div class="swatch"><div class="swatch-color" style="background:${theme[key]}"></div><strong>${title(key)}</strong><code>${theme[key]}</code></div>
  `).join("");

  const checks = ["foreground", "brightBlack", "red", "green", "yellow", "blue", "purple", "cyan"];
  document.querySelector("#contrast-results").innerHTML = checks.map(key => {
    const ratio = contrast(theme[key], theme.background);
    return `<div class="contrast ${ratio >= 4.5 ? "pass" : "warn"}"><strong>${ratio.toFixed(2)}:1</strong><span>${title(key)} / background</span></div>`;
  }).join("");
}

async function save() {
  theme.name = document.querySelector("#theme-name").value.trim();
  const response = await fetch("/api/theme", { method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(theme) });
  const result = await response.json();
  if (!response.ok) return alert(result.error);
  theme = result;
  original = structuredClone(result);
  document.querySelector("#status").textContent = "Saved";
}

function download() {
  theme.name = document.querySelector("#theme-name").value.trim();
  const blob = new Blob([JSON.stringify(theme, null, 2) + "\n"], {type: "application/json"});
  const link = Object.assign(document.createElement("a"), {href: URL.createObjectURL(blob), download: "nova.windows-terminal.json"});
  link.click();
  URL.revokeObjectURL(link.href);
}

async function start() {
  theme = await fetch("/api/theme").then(response => response.json());
  original = structuredClone(theme);
  document.querySelector("#theme-name").value = theme.name;
  renderControls();
  renderPreview();
  document.querySelector("#status").textContent = "Saved palette";
}

document.querySelector("#save").addEventListener("click", save);
document.querySelector("#download").addEventListener("click", download);
document.querySelector("#reset").addEventListener("click", () => {
  theme = structuredClone(original);
  document.querySelector("#theme-name").value = theme.name;
  renderControls();
  renderPreview();
  document.querySelector("#status").textContent = "Draft reset";
});

start().catch(error => {
  document.querySelector("#status").textContent = "Failed to load";
  console.error(error);
});

