(function () {
  var mount = document.getElementById("tracker");
  if (!mount) return;
  var KEY = "cc-progress-v1";
  var DATA = null;
  var state = JSON.parse(localStorage.getItem(KEY) || "{}");

  function save() { localStorage.setItem(KEY, JSON.stringify(state)); }
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x !== undefined) n.textContent = x; return n; }
  function slugOf(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, "-"); }

  function render(slug) {
    var exam = DATA.exams[slug];
    var mine = state[slug] || (state[slug] = { domains: {}, milestones: {} });
    mount.innerHTML = "";

    var card = el("div", "quiz__card");

    var pick = el("select", "quiz__select");
    pick.setAttribute("aria-label", "Certification");
    Object.keys(DATA.exams).forEach(function (s) {
      var o = el("option", null, DATA.exams[s].title);
      o.value = s;
      if (s === slug) o.selected = true;
      pick.appendChild(o);
    });
    pick.addEventListener("change", function () { render(pick.value); });
    card.appendChild(pick);

    var covered = 0, total = 0;
    exam.domains.forEach(function (d) {
      total += d.weight;
      if (mine.domains[slugOf(d.name)]) covered += d.weight;
    });
    var pct = total ? Math.round(100 * covered / total) : 0;
    var doneMiles = exam.milestones.filter(function (m) { return mine.milestones[slugOf(m)]; }).length;

    var head = el("div", "quiz__meta");
    head.appendChild(el("span", null, "Blueprint covered, weighted by exam share"));
    head.appendChild(el("span", "quiz__timer", pct + "%"));
    card.appendChild(head);

    var bar = el("div", "quiz__bar");
    var fill = el("div", "quiz__bar-fill");
    fill.style.width = pct + "%";
    bar.appendChild(fill);
    card.appendChild(bar);

    var verdict = pct >= 90 ? "Ready to book, if a timed mock agrees."
      : pct >= 70 ? "Close. Finish the remaining domains, then sit a mock exam."
      : pct >= 40 ? "Halfway. Keep working the heaviest uncovered domains first."
      : "Early. Start with the domains carrying the most weight.";
    card.appendChild(el("p", "quiz__review-r", verdict));

    card.appendChild(el("h3", "quiz__title", "Domains"));
    exam.domains.forEach(function (d) {
      var id = slugOf(d.name);
      var row = el("label", "tracker__row");
      var box = document.createElement("input");
      box.type = "checkbox";
      box.checked = !!mine.domains[id];
      box.addEventListener("change", function () {
        mine.domains[id] = box.checked;
        save();
        render(slug);
      });
      row.appendChild(box);
      row.appendChild(el("span", "tracker__label", d.name));
      row.appendChild(el("span", "tracker__weight", d.weight + "%"));
      card.appendChild(row);
    });

    card.appendChild(el("h3", "quiz__title", "Milestones  ·  " + doneMiles + " of " + exam.milestones.length));
    exam.milestones.forEach(function (m) {
      var id = slugOf(m);
      var row = el("label", "tracker__row");
      var box = document.createElement("input");
      box.type = "checkbox";
      box.checked = !!mine.milestones[id];
      box.addEventListener("change", function () {
        mine.milestones[id] = box.checked;
        save();
        render(slug);
      });
      row.appendChild(box);
      row.appendChild(el("span", "tracker__label", m));
      card.appendChild(row);
    });

    var reset = el("button", "quiz__button", "Reset this exam");
    reset.type = "button";
    reset.addEventListener("click", function () {
      if (confirm("Clear your saved progress for this certification?")) {
        delete state[slug];
        save();
        render(slug);
      }
    });
    card.appendChild(reset);
    mount.appendChild(card);
  }

  fetch("../assets/tracker.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { DATA = data; var first = Object.keys(data.exams); render(first[0]); })
    .catch(function () {
      mount.appendChild(el("p", null, "The tracker data could not be loaded. The printable checklist is in the study strategy."));
    });
})();
