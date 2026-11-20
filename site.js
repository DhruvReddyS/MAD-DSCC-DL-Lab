// Renders the lab programs from the JSON embedded in index.html.
// URL hash = #subject/program (e.g. #dscc/exp07) so the last view is remembered.
(function () {
  const subjects = JSON.parse(document.getElementById("data").textContent);
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, html) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  };

  function store(k, v) {
    try { v === undefined ? (v = localStorage.getItem(k)) : localStorage.setItem(k, v); } catch (e) { v = null; }
    return v;
  }

  function parseHash() {
    const [s, p] = location.hash.replace(/^#/, "").split("/");
    const subj = subjects.find((x) => x.id === s);
    if (!subj) return null;
    const prog = subj.programs.find((x) => x.id === p) || subj.programs[0];
    return { subj, prog };
  }

  function copyText(text, btn) {
    const done = () => {
      btn.textContent = "Copied ✓"; btn.classList.add("done");
      setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("done"); }, 1500);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, () => fallback());
    } else fallback();
    function fallback() {
      const t = document.createElement("textarea");
      t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      try { document.execCommand("copy"); done(); } catch (e) { btn.textContent = "Select & copy"; }
      t.remove();
    }
  }

  function codeBlock(name, code, lang, extraCls) {
    const box = el("div", "file" + (extraCls ? " " + extraCls : ""));
    const head = el("div", "file-head");
    head.appendChild(el("span", "file-name")).textContent = name;
    const btn = el("button", "copy"); btn.type = "button"; btn.textContent = "Copy";
    btn.addEventListener("click", () => copyText(code, btn));
    head.appendChild(btn);
    const pre = el("pre"); const c = el("code", lang ? "language-" + lang : "");
    c.textContent = code; pre.appendChild(c);
    box.append(head, pre);
    if (window.Prism && lang && lang !== "none" && Prism.languages[lang]) Prism.highlightElement(c);
    return box;
  }

  function list(items) {
    const ol = el("ol");
    items.forEach((t) => ol.appendChild(el("li", null, t)));
    return ol;
  }

  function renderTabs(active) {
    const tabs = $("tabs"); tabs.innerHTML = "";
    subjects.forEach((s) => {
      const b = el("button"); b.type = "button"; b.textContent = s.name; b.title = s.full;
      b.setAttribute("role", "tab"); b.setAttribute("aria-selected", s.id === active.id);
      b.addEventListener("click", () => {
        const last = store("last-" + s.id);
        location.hash = s.id + "/" + (last || s.programs[0].id);
      });
      tabs.appendChild(b);
    });
  }

  function renderSide(subj, prog) {
    const side = $("side"); side.innerHTML = "";
    side.appendChild(el("h2")).textContent = subj.name;
    side.appendChild(el("p", "full")).textContent = subj.full;
    subj.programs.forEach((p) => {
      const a = el("a"); a.href = "#" + subj.id + "/" + p.id; a.textContent = p.title;
      if (p.id === prog.id) a.className = "active";
      a.addEventListener("click", () => side.classList.remove("open"));
      side.appendChild(a);
    });
  }

  function renderMain(subj, prog) {
    const m = $("main"); m.innerHTML = "";
    if (subj.procedure) {
      const d = el("details", "proc"); const saved = store("proc-open");
      d.open = saved ? saved === "1" : window.innerWidth > 820; // collapsed by default on phones
      d.appendChild(el("summary", null, "Common steps: run any MAD program in Android Studio"));
      d.appendChild(list(subj.procedure));
      d.addEventListener("toggle", () => store("proc-open", d.open ? "1" : "0"));
      m.appendChild(d);
    }
    m.appendChild(el("h1")).textContent = prog.title;
    if (prog.question) m.appendChild(el("p", "question")).textContent = "Q: " + prog.question;
    m.appendChild(el("div", "card aim", "<b>Aim:</b> " + prog.aim));

    if (prog.theory) {
      m.appendChild(el("h3", null, "Theory"));
      m.appendChild(list(prog.theory));
    }

    m.appendChild(el("h3", null, "How to run"));
    m.appendChild(list(prog.run));

    if (prog.manifest_add) {
      m.appendChild(el("h3", null, "Manifest lines to add"));
      m.appendChild(codeBlock("AndroidManifest.xml (add these)", prog.manifest_add, "markup"));
    }

    m.appendChild(el("h3", null, prog.files.length > 1 ? "Program files" : "Program"));
    prog.files.forEach((f) => m.appendChild(codeBlock(f.name, f.code, f.lang)));

    const ok = /^(Ran|Tested)/.test(prog.output.badge);
    m.appendChild(el("h3", null, "Output <span class='badge " + (ok ? "ok" : "warn") + "'></span>"))
      .querySelector(".badge").textContent = prog.output.badge;
    m.appendChild(codeBlock("Output", prog.output.text, "none", "output"));

    const i = subj.programs.indexOf(prog);
    const pager = el("div", "pager");
    const prev = subj.programs[i - 1], next = subj.programs[i + 1];
    pager.appendChild(prev ? Object.assign(el("a"), { href: "#" + subj.id + "/" + prev.id, textContent: "← " + prev.title }) : el("span"));
    pager.appendChild(next ? Object.assign(el("a"), { href: "#" + subj.id + "/" + next.id, textContent: next.title + " →" }) : el("span"));
    m.appendChild(pager);
  }

  function render() {
    let r = parseHash();
    if (!r) {
      const saved = store("last-view");
      location.replace("#" + (saved || subjects[0].id + "/" + subjects[0].programs[0].id));
      r = parseHash() || { subj: subjects[0], prog: subjects[0].programs[0] };
    }
    store("last-view", r.subj.id + "/" + r.prog.id);
    store("last-" + r.subj.id, r.prog.id);
    document.title = r.prog.title + " · " + r.subj.name + " Lab Programs";
    renderTabs(r.subj); renderSide(r.subj, r.prog); renderMain(r.subj, r.prog);
    window.scrollTo(0, 0);
  }

  $("menuBtn").addEventListener("click", () => $("side").classList.toggle("open"));
  window.addEventListener("hashchange", render);
  render();
})();

// light / dark toggle (dark is default)
(function () {
  const btn = document.getElementById("themeBtn");
  const root = document.documentElement;
  const paint = () => { btn.textContent = root.dataset.theme === "light" ? "🌙 Dark" : "☀️ Light"; };
  btn.addEventListener("click", () => {
    if (root.dataset.theme === "light") delete root.dataset.theme; else root.dataset.theme = "light";
    try { localStorage.setItem("theme", root.dataset.theme || "dark"); } catch (e) {}
    paint();
  });
  paint();
})();
