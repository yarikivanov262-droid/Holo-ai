const toast = document.querySelector('#toast');
let toastTimer;
function announce(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

document.querySelector('#demoButton').addEventListener('click', () => {
  announce('Это статический UI-мокап. Подключение к игре отключено.');
});
document.querySelector('#refreshButton').addEventListener('click', () => {
  announce('Показаны демонстрационные статусы модулей.');
});
document.querySelectorAll('.nav-item').forEach((item) => {
  item.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach((link) => link.classList.remove('active'));
    item.classList.add('active');
  });
});
