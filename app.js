// Wayfinder case-study page: theme toggle and a filterable view of the evaluation set.
(function () {
  "use strict";

  // Theme ----------------------------------------------------------------
  const root = document.documentElement;
  const toggle = document.getElementById("theme");
  const stored = localStorage.getItem("wayfinder-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  let theme = stored || (prefersDark ? "dark" : "light");

  function applyTheme() {
    root.dataset.theme = theme;
    toggle.textContent = theme === "dark" ? "Light" : "Dark";
    localStorage.setItem("wayfinder-theme", theme);
  }

  toggle.addEventListener("click", function () {
    theme = theme === "dark" ? "light" : "dark";
    applyTheme();
  });
  applyTheme();

  // Evaluation set --------------------------------------------------------
  const list = document.getElementById("cases");
  const filter = document.getElementById("filter");
  const count = document.getElementById("count");
  let all = [];

  function render(query) {
    const q = query.trim().toLowerCase();
    const matches = all.filter(function (item) {
      if (!q) return true;
      return (
        item.question.toLowerCase().includes(q) ||
        item.relevant_chunk_ids.some(function (id) { return id.toLowerCase().includes(q); })
      );
    });

    count.textContent = matches.length + " of " + all.length + " questions";
    list.replaceChildren();

    if (matches.length === 0) {
      const empty = document.createElement("li");
      empty.className = "empty";
      empty.textContent = "No questions match that filter.";
      list.appendChild(empty);
      return;
    }

    matches.forEach(function (item, index) {
      const li = document.createElement("li");
      li.style.animationDelay = Math.min(index * 20, 300) + "ms";

      const question = document.createElement("p");
      question.className = "q";
      question.textContent = item.question;

      const chips = document.createElement("div");
      chips.className = "chips";
      item.relevant_chunk_ids.forEach(function (id) {
        const chip = document.createElement("span");
        chip.className = "chip";
        chip.textContent = id;
        chips.appendChild(chip);
      });

      li.append(question, chips);
      list.appendChild(li);
    });
  }

  fetch("cases.json")
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (data) {
      all = data;
      render("");
    })
    .catch(function () {
      count.textContent = "The evaluation set could not be loaded.";
    });

  filter.addEventListener("input", function (event) {
    render(event.target.value);
  });
})();
