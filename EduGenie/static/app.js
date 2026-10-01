const task = document.getElementById("task");
const level = document.getElementById("level");
const levelWrap = document.getElementById("level-wrap");
const input = document.getElementById("input");
const inputLabel = document.getElementById("input-label");
const extraControls = document.getElementById("extra-controls");
const submitBtn = document.getElementById("submit-btn");
const statusEl = document.getElementById("status");
const resultCard = document.getElementById("result-card");
const resultEl = document.getElementById("result");
const resultTitle = document.getElementById("result-title");
const copyBtn = document.getElementById("copy-btn");

const configs = {
  qa: {
    label: "Your question",
    placeholder: "Example: What is the largest ocean?",
    button: "Ask EduGenie",
    title: "Answer",
    endpoint: "/qa",
  },
  explain: {
    label: "Topic to explain",
    placeholder: "Example: Explain the Pythagoras theorem",
    button: "Explain Topic",
    title: "Explanation",
    endpoint: "/explain",
  },
  quiz: {
    label: "Topic or passage",
    placeholder: "Paste a lesson, paragraph, or topic here...",
    button: "Generate Quiz",
    title: "Quiz",
    endpoint: "/quiz",
  },
  summarize: {
    label: "Text to summarize",
    placeholder: "Paste your notes or educational passage here...",
    button: "Summarize",
    title: "Summary",
    endpoint: "/summarize",
  },
  learn: {
    label: "Topic for your learning path",
    placeholder: "Example: SQL",
    button: "Build Learning Path",
    title: "Learning Path",
    endpoint: "/learn/recommendations",
  }
};

function updateForm() {
  const cfg = configs[task.value];
  inputLabel.textContent = cfg.label;
  input.placeholder = cfg.placeholder;
  submitBtn.textContent = cfg.button;
  resultTitle.textContent = cfg.title;

  levelWrap.style.display = task.value === "qa" ? "none" : "block";

  extraControls.innerHTML = "";
  if (task.value === "quiz") {
    const wrapper = document.createElement("label");
    wrapper.innerHTML = `
      <span>Number of questions</span>
      <select id="count">
        <option value="3">3</option>
        <option value="5">5</option>
        <option value="10">10</option>
      </select>`;
    extraControls.appendChild(wrapper);
  } else if (task.value === "summarize") {
    const wrapper = document.createElement("label");
    wrapper.innerHTML = `
      <span>Maximum words</span>
      <select id="maxWords">
        <option value="80">80</option>
        <option value="120" selected>120</option>
        <option value="200">200</option>
        <option value="300">300</option>
      </select>`;
    extraControls.appendChild(wrapper);
  } else if (task.value === "learn") {
    const wrapper = document.createElement("label");
    wrapper.innerHTML = `
      <span>Timeline</span>
      <select id="timeline">
        <option>2 weeks</option>
        <option selected>4 weeks</option>
        <option>8 weeks</option>
        <option>12 weeks</option>
      </select>`;
    extraControls.appendChild(wrapper);
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderText(text) {
  resultEl.innerHTML = `<div>${escapeHtml(text).replaceAll("\n", "<br>")}</div>`;
}

function renderQuiz(quiz) {
  resultEl.innerHTML = "";
  quiz.questions.forEach((item, index) => {
    const box = document.createElement("div");
    box.className = "quiz-question";
    box.innerHTML = `
      <h3>Q${index + 1}. ${escapeHtml(item.question)}</h3>
      <div class="quiz-options"></div>
      <p class="feedback" id="feedback-${index}"></p>`;
    const options = box.querySelector(".quiz-options");

    item.options.forEach(option => {
      const btn = document.createElement("button");
      btn.className = "quiz-option";
      btn.textContent = option;
      btn.addEventListener("click", () => {
        [...options.children].forEach(b => b.disabled = true);
        if (option === item.answer) {
          btn.classList.add("correct");
          box.querySelector(".feedback").textContent = `✓ Correct. ${item.explanation}`;
        } else {
          btn.classList.add("wrong");
          box.querySelector(".feedback").textContent =
            `✗ Not quite. Correct answer: ${item.answer}. ${item.explanation}`;
          [...options.children].find(b => b.textContent === item.answer)?.classList.add("correct");
        }
      });
      options.appendChild(btn);
    });
    resultEl.appendChild(box);
  });
}

function buildPayload() {
  const value = input.value.trim();
  if (!value) throw new Error("Please enter some content first.");

  switch (task.value) {
    case "qa":
      return { question: value };
    case "explain":
      return { topic: value, level: level.value };
    case "quiz":
      return { text: value, count: Number(document.getElementById("count").value) };
    case "summarize":
      return { text: value, max_words: Number(document.getElementById("maxWords").value) };
    case "learn":
      return {
        topic: value,
        level: level.value,
        timeline: document.getElementById("timeline").value
      };
  }
}

async function submit() {
  statusEl.textContent = "EduGenie is thinking...";
  statusEl.className = "status";
  submitBtn.disabled = true;

  try {
    const cfg = configs[task.value];
    const response = await fetch(cfg.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildPayload())
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    resultCard.classList.remove("hidden");
    if (task.value === "qa") renderText(data.answer);
    if (task.value === "explain") renderText(data.explanation);
    if (task.value === "summarize") renderText(data.summary);
    if (task.value === "learn") renderText(data.learning_path);
    if (task.value === "quiz") renderQuiz(data.quiz);

    statusEl.textContent = "Done.";
  } catch (error) {
    statusEl.textContent = error.message;
    statusEl.className = "status error";
  } finally {
    submitBtn.disabled = false;
  }
}

task.addEventListener("change", updateForm);
submitBtn.addEventListener("click", submit);

copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(resultEl.innerText);
  copyBtn.textContent = "Copied!";
  setTimeout(() => copyBtn.textContent = "Copy", 1200);
});

updateForm();
