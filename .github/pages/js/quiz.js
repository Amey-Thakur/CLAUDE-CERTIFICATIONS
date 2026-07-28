(function () {
  var mount = document.getElementById("quiz-app");
  if (!mount) return;
  var BANK = null, state = null;
  var LETTERS = ["A", "B", "C", "D"];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }
  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
    return list;
  }

  function start(slug, count) {
    var pool = BANK.questions.filter(function (q) { return q.exam === slug; });
    var picked = shuffle(pool.slice()).slice(0, Math.min(count, pool.length));
    var questions = picked.map(function (q) {
      var pairs = shuffle(Object.keys(q.options).sort().map(function (k) {
        return { text: q.options[k], correct: k === q.answer };
      }));
      return { q: q, pairs: pairs, answer: pairs.findIndex(function (p) { return p.correct; }), given: null };
    });
    state = { slug: slug, questions: questions, index: 0, started: Date.now() };
    render();
  }

  function renderStart() {
    mount.innerHTML = "";
    var card = el("div", "quiz__card");
    card.appendChild(el("h2", "quiz__title", "Start a practice exam"));

    var examLabel = el("label", "quiz__label", "Certification");
    examLabel.setAttribute("for", "quiz-exam");
    var exam = el("select", "quiz__select");
    exam.id = "quiz-exam";
    Object.keys(BANK.exams).forEach(function (slug) {
      var o = el("option", null, BANK.exams[slug].title + " (" + BANK.exams[slug].count + " in bank)");
      o.value = slug;
      exam.appendChild(o);
    });

    var countLabel = el("label", "quiz__label", "Questions");
    countLabel.setAttribute("for", "quiz-count");
    var count = el("select", "quiz__select");
    count.id = "quiz-count";
    [5, 10, 15, 25].forEach(function (n) {
      var o = el("option", null, String(n));
      o.value = n;
      if (n === 15) o.selected = true;
      count.appendChild(o);
    });

    var go = el("button", "quiz__button quiz__button--primary", "Start");
    go.type = "button";
    go.addEventListener("click", function () { start(exam.value, parseInt(count.value, 10)); });

    card.appendChild(examLabel); card.appendChild(exam);
    card.appendChild(countLabel); card.appendChild(count);
    card.appendChild(go);
    mount.appendChild(card);
  }

  function render(keepScroll) {
    var item = state.questions[state.index];
    mount.innerHTML = "";
    var card = el("div", "quiz__card");

    var meta = el("div", "quiz__meta");
    meta.appendChild(el("span", null, "Question " + (state.index + 1) + " of " + state.questions.length));
    var timer = el("span", "quiz__timer", "0:00");
    meta.appendChild(timer);
    card.appendChild(meta);

    var bar = el("div", "quiz__bar");
    var fill = el("div", "quiz__bar-fill");
    fill.style.width = Math.round(100 * state.index / state.questions.length) + "%";
    bar.appendChild(fill);
    card.appendChild(bar);

    card.appendChild(el("p", "quiz__question", item.q.question));

    var list = el("div", "quiz__options");
    item.pairs.forEach(function (pair, i) {
      var b = el("button", "quiz__option", LETTERS[i] + ". " + pair.text);
      b.type = "button";
      if (item.given === i) b.classList.add("is-selected");
      b.addEventListener("click", function () { item.given = i; render(true); });
      list.appendChild(b);
    });
    card.appendChild(list);

    var nav = el("div", "quiz__nav");
    if (state.index > 0) {
      var back = el("button", "quiz__button", "Back");
      back.type = "button";
      back.addEventListener("click", function () { state.index--; render(); });
      nav.appendChild(back);
    }
    var isLast = state.index === state.questions.length - 1;
    var next = el("button", "quiz__button quiz__button--primary", isLast ? "Finish" : "Next");
    next.type = "button";
    next.addEventListener("click", function () {
      if (isLast) { results(); } else { state.index++; render(); }
    });
    nav.appendChild(next);
    card.appendChild(nav);
    mount.appendChild(card);
    if (!keepScroll) card.scrollIntoView({ behavior: "smooth", block: "start" });

    if (state.tick) clearInterval(state.tick);
    state.tick = setInterval(function () {
      var s = Math.floor((Date.now() - state.started) / 1000);
      timer.textContent = Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
    }, 1000);
  }

  function results() {
    if (state.tick) clearInterval(state.tick);
    var right = 0, byDomain = {};
    state.questions.forEach(function (item) {
      var ok = item.given === item.answer;
      if (ok) right++;
      var d = byDomain[item.q.domain] || (byDomain[item.q.domain] = { got: 0, asked: 0 });
      d.asked++; if (ok) d.got++;
    });
    var total = state.questions.length;
    var seconds = Math.floor((Date.now() - state.started) / 1000);

    mount.innerHTML = "";
    var card = el("div", "quiz__card");
    card.appendChild(el("h2", "quiz__title", right + " of " + total + " correct (" + Math.round(100 * right / total) + "%)"));
    card.appendChild(el("p", "quiz__meta", "Time " + Math.floor(seconds / 60) + "m " + (seconds % 60) + "s"));

    var table = el("table", "quiz__table");
    var head = el("tr");
    head.appendChild(el("th", null, "Domain"));
    head.appendChild(el("th", null, "Score"));
    table.appendChild(head);
    Object.keys(byDomain).sort(function (a, b) {
      return byDomain[a].got / byDomain[a].asked - byDomain[b].got / byDomain[b].asked;
    }).forEach(function (d) {
      var tr = el("tr");
      tr.appendChild(el("td", null, d));
      tr.appendChild(el("td", null, byDomain[d].got + "/" + byDomain[d].asked));
      table.appendChild(tr);
    });
    card.appendChild(table);

    state.questions.forEach(function (item, n) {
      var ok = item.given === item.answer;
      var block = el("div", "quiz__review " + (ok ? "is-right" : "is-wrong"));
      block.appendChild(el("p", "quiz__review-q", (n + 1) + ". " + item.q.question));
      item.pairs.forEach(function (pair, i) {
        var note = "";
        if (i === item.answer) note = "  (correct)";
        else if (i === item.given) note = "  (your answer)";
        var line = el("p", "quiz__review-o", LETTERS[i] + ". " + pair.text + note);
        if (i === item.answer) line.classList.add("is-answer");
        block.appendChild(line);
      });
      block.appendChild(el("p", "quiz__review-r", item.q.rationale));
      card.appendChild(block);
    });

    var again = el("button", "quiz__button quiz__button--primary", "New exam");
    again.type = "button";
    again.addEventListener("click", renderStart);
    card.appendChild(again);
    mount.appendChild(card);
    mount.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  fetch("../assets/question-bank.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { BANK = data; renderStart(); })
    .catch(function () {
      mount.appendChild(el("p", null, "The question bank could not be loaded. Use the command line runner below."));
    });
})();
