(function () {
  var mount = document.getElementById("taster");
  if (!mount) return;
  var LETTERS = ["A", "B", "C", "D"];
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x !== undefined) n.textContent = x; return n; }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  fetch("assets/question-bank.json").then(function (r) { return r.json(); }).then(function (bank) {
    var q = bank.questions[Math.floor(Math.random() * bank.questions.length)];
    var pairs = shuffle(Object.keys(q.options).sort().map(function (k) {
      return { text: q.options[k], correct: k === q.answer };
    }));
    var card = el("div", "quiz__card");
    card.appendChild(el("p", "quiz__meta", bank.exams[q.exam].title + "  ·  " + q.domain));
    card.appendChild(el("p", "quiz__question", q.question));
    var list = el("div", "quiz__options");
    var done = false;
    pairs.forEach(function (pair, i) {
      var b = el("button", "quiz__option", LETTERS[i] + ". " + pair.text);
      b.type = "button";
      b.addEventListener("click", function () {
        if (done) return;
        done = true;
        pairs.forEach(function (p2, j) {
          var node = list.children[j];
          if (p2.correct) node.classList.add("is-correct");
          else if (j === i) node.classList.add("is-incorrect");
        });
        var verdict = el("p", "quiz__review-r", (pair.correct ? "Correct. " : "Not quite. ") + q.rationale);
        card.insertBefore(verdict, foot);
      });
      list.appendChild(b);
    });
    card.appendChild(list);
    var foot = el("p", "quiz__meta");
    var more = el("a", null, "Take a full practice exam");
    more.href = "guide/quiz.html";
    foot.appendChild(more);
    foot.appendChild(document.createTextNode("  ·  320 questions across the four certifications"));
    card.appendChild(foot);
    mount.appendChild(card);
  }).catch(function () {
    var p = el("p");
    var a = el("a", null, "Open the practice engine");
    a.href = "guide/quiz.html";
    p.appendChild(a);
    mount.appendChild(p);
  });
})();
