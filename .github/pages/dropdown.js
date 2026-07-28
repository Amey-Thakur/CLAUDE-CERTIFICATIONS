/* Themed dropdowns.

   A native select paints its open list with the operating system's own colors,
   which on Windows is a blue that belongs to no part of this site. This
   replaces every select the widgets create with a listbox built from ordinary
   elements, so it takes the page's palette in both color schemes.

   The original select stays in the document, hidden but intact, and every
   change is dispatched on it. Widget code keeps reading and writing
   select.value and listening for change, exactly as it did before. If this
   script does not run, the native select is still there and still works. */

(function () {
  "use strict";

  function upgrade(select) {
    if (select.dataset.themed === "1") return;
    select.dataset.themed = "1";

    var root = document.createElement("div");
    root.className = "pick";

    var button = document.createElement("button");
    button.type = "button";
    button.className = "pick__button";
    button.setAttribute("aria-haspopup", "listbox");
    button.setAttribute("aria-expanded", "false");
    var label = select.getAttribute("aria-label");
    if (label) button.setAttribute("aria-label", label);

    var text = document.createElement("span");
    text.className = "pick__value";
    button.appendChild(text);

    var caret = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    caret.setAttribute("class", "pick__caret");
    caret.setAttribute("viewBox", "0 0 12 8");
    caret.setAttribute("aria-hidden", "true");
    var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M1 1.5 6 6.5 11 1.5");
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "currentColor");
    path.setAttribute("stroke-width", "1.6");
    path.setAttribute("stroke-linecap", "round");
    path.setAttribute("stroke-linejoin", "round");
    caret.appendChild(path);
    button.appendChild(caret);

    var list = document.createElement("div");
    list.className = "pick__list";
    list.setAttribute("role", "listbox");
    if (label) list.setAttribute("aria-label", label);
    list.hidden = true;

    var items = [];

    function sync() {
      var i = select.selectedIndex < 0 ? 0 : select.selectedIndex;
      text.textContent = select.options[i] ? select.options[i].textContent : "";
      items.forEach(function (item, n) {
        var on = n === i;
        item.classList.toggle("is-selected", on);
        item.setAttribute("aria-selected", on ? "true" : "false");
      });
    }

    [].forEach.call(select.options, function (option, n) {
      var item = document.createElement("div");
      item.className = "pick__option";
      item.setAttribute("role", "option");
      item.tabIndex = -1;
      item.textContent = option.textContent;
      item.addEventListener("click", function () {
        select.selectedIndex = n;
        sync();
        close(true);
        select.dispatchEvent(new Event("change", { bubbles: true }));
      });
      items.push(item);
      list.appendChild(item);
    });

    function open() {
      if (!list.hidden) return;
      list.hidden = false;
      button.setAttribute("aria-expanded", "true");
      var current = items[select.selectedIndex < 0 ? 0 : select.selectedIndex];
      if (current) {
        current.focus();
        current.scrollIntoView({ block: "nearest" });
      }
      document.addEventListener("mousedown", away, true);
    }

    function close(focusButton) {
      if (list.hidden) return;
      list.hidden = true;
      button.setAttribute("aria-expanded", "false");
      document.removeEventListener("mousedown", away, true);
      if (focusButton) button.focus();
    }

    function away(e) {
      if (!root.contains(e.target)) close(false);
    }

    function move(from, step) {
      var next = from + step;
      if (next < 0) next = items.length - 1;
      if (next >= items.length) next = 0;
      items[next].focus();
      return next;
    }

    button.addEventListener("click", function () {
      if (list.hidden) open(); else close(false);
    });

    button.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });

    list.addEventListener("keydown", function (e) {
      var at = items.indexOf(document.activeElement);
      if (at < 0) return;
      if (e.key === "ArrowDown") { e.preventDefault(); move(at, 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(at, -1); }
      else if (e.key === "Home") { e.preventDefault(); items[0].focus(); }
      else if (e.key === "End") { e.preventDefault(); items[items.length - 1].focus(); }
      else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); items[at].click(); }
      else if (e.key === "Escape" || e.key === "Tab") { close(e.key === "Escape"); }
    });

    // Widget code may set select.value directly; keep the button in step.
    select.addEventListener("change", sync);

    select.classList.add("pick__native");
    select.parentNode.insertBefore(root, select);
    root.appendChild(button);
    root.appendChild(list);
    root.appendChild(select);
    sync();
  }

  function scan() {
    [].forEach.call(document.querySelectorAll("select.quiz__select"), upgrade);
  }

  // The widgets redraw themselves, so watch for selects that appear later.
  function watch() {
    scan();
    if (!window.MutationObserver) return;
    new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", watch);
  } else {
    watch();
  }
})();
