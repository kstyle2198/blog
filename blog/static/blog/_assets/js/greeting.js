const form = document.querySelector('.js-form'),
  input = form.querySelector('input'),
  greeting = document.querySelector('.js-greetings');

const USER_LS = 'currentUser',
  SHOWING_CN = 'showing';

function saveName(text) {
  localStorage.setItem(USER_LS, text);
}

function paintGreeting(text) {
  form.classList.remove(SHOWING_CN);
  greeting.classList.add(SHOWING_CN);
  greeting.innerHTML = `Good Day! ${text}`;
}

function handleSubmit(event) {
  event.preventDefault(); //이름 입력후 엔터칠 때, 창 새로고침 하지 않도록
  const currentValue = input.value; // 인풋 상자의 값을 받아라...
  paintGreeting(currentValue);
  saveName(currentValue); // 새로고침을 해도 이름을 기억할 수 있게 세이브 함수를 만들어서 호출(디바이드 앤 퀑커)
}

function askForName() {
  form.classList.add(SHOWING_CN);
  form.addEventListener('submit', handleSubmit);
}

function loadName() {
  const currentUser = localStorage.getItem(USER_LS);
  if (currentUser === null) {
    askForName();
  } else {
    paintGreeting(currentUser);
  }
}

function init() {
  loadName();
}

init();
