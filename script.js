// Переключение темы
const themeToggle = document.getElementById("theme-toggle");
themeToggle?.addEventListener("click", () => {
  document.body.classList.toggle("theme-dark");
  localStorage.setItem("theme", document.body.classList.contains("theme-dark") ? "dark" : "light");
});

// Установка темы при загрузке
window.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("theme-dark");
  }
});

// Показ комментариев
document.querySelectorAll(".comment-toggle").forEach((btn) => {
  btn.addEventListener("click", () => {
    const commentBox = btn.nextElementSibling;
    commentBox.classList.toggle("hidden");
  });
});

// Обработка формы входа
const loginForm = document.getElementById("login-form");
loginForm?.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = loginForm.email.value;
  const password = loginForm.password.value;

  // Здесь должен быть запрос на сервер
  alert(`Вход выполнен как ${email}`);
});

// Обработка формы регистрации
const registerForm = document.getElementById("register-form");
registerForm?.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = registerForm.name.value;
  const email = registerForm.email.value;
  const password = registerForm.password.value;

  // Здесь должен быть запрос на сервер
  alert(`Регистрация пользователя ${name}`);
});

// Переключение между страницами (просто пример)
function showPage(id) {
  document.querySelectorAll(".page").forEach((el) => el.classList.add("hidden"));
  document.getElementById(id)?.classList.remove("hidden");
}

// FPS консоль
let showFPS = false;
const fpsCounter = document.createElement("div");
fpsCounter.style.position = "fixed";
fpsCounter.style.top = "10px";
fpsCounter.style.right = "10px";
fpsCounter.style.padding = "4px 8px";
fpsCounter.style.background = "#000";
fpsCounter.style.color = "#0f0";
fpsCounter.style.fontFamily = "monospace";
fpsCounter.style.fontSize = "14px";
fpsCounter.style.zIndex = "10000";
fpsCounter.style.display = "none";
document.body.appendChild(fpsCounter);

let lastTime = performance.now();
let frames = 0;

function updateFPS() {
  const now = performance.now();
  frames++;
  if (now - lastTime >= 1000) {
    fpsCounter.textContent = `FPS: ${frames}`;
    frames = 0;
    lastTime = now;
  }
  if (showFPS) requestAnimationFrame(updateFPS);
}
updateFPS();

document.addEventListener("keydown", (e) => {
  if (e.key === "ё") {
    const input = prompt("Введите команду:");
    if (input === "fps") {
      showFPS = !showFPS;
      fpsCounter.style.display = showFPS ? "block" : "none";
      if (showFPS) updateFPS();
    }
  }
});

