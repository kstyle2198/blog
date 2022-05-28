const toDoForm = document.querySelector('.js-toDoForm'),
  toDoInput = toDoForm.querySelector('input'),
  toDoList = document.querySelector('.js-toDoList');

const TODOS_LS = 'toDos';

let toDos = []; // 투두 리스트를 저장하기 위한 어레이

function deleteToDO(event) {
  // console.dir(event.target);   // id를 보여주는 값을 찾기 위해
  // console.log(event.target.parentNode);
  const btn = event.target;
  const li = btn.parentNode;
  toDoList.removeChild(li); //HTML상 제거는 여기서 가능
  // 아래에서 로컬스토리지에서 제거하는 기능 구현
  const cleanToDos = toDos.filter(function (toDo) {
    // 필터는 매행 검토하여 트루인 것만 골라서 새 어레이를 만든다.
    return toDo.id !== parseInt(li.id); // li.id가 스트링이기 때문에 넘버로 타입 변경
  });
  toDos = cleanToDos;
  saveToDos();
}

function saveToDos() {
  localStorage.setItem(TODOS_LS, JSON.stringify(toDos));
  /* 로컬스토리지에는 오직 스트링만 저장 가능하기 때문에.. 자바스크립트 그 자체로는 저장 안된다.
    자바스크립트를 스트링으로 바뀌기 위한 json stringify를 사용한다.*/
}

function paintToDo(text) {
  // console.log(text);
  const li = document.createElement('li'); //HTML에 엘레멘트를 생성하는 함수
  const delBt = document.createElement('button');
  const span = document.createElement('span');
  const newId = toDos.length + 1; // 새 아이디는 직전 개수 + 1의 숫자이다.
  delBt.innerText = '✖';
  delBt.addEventListener('click', deleteToDO);
  span.innerText = text;
  li.appendChild(span); // li 안에 자식으로 뭘 만들어라
  li.appendChild(delBt);
  li.id = newId; // li의 자식이 아니라 li 자체의 id 값을 설정
  toDoList.appendChild(li);
  const toDoObj = {
    text: text,
    id: newId,
  };
  toDos.push(toDoObj);
  saveToDos();
}

function handleSubmit(event) {
  event.preventDefault();
  const currentValue = toDoInput.value;
  paintToDo(currentValue);
  toDoInput.value = ''; // 값 입력후 엔터치면 인풋 상자 공란으로
}

function loadToDos() {
  const loadToDos = localStorage.getItem(TODOS_LS);
  if (loadToDos !== null) {
    // console.log(loadToDos);
    const parsedToDos = JSON.parse(loadToDos); // 스트링을 자바스크립트로 변경하기 위해 json parse 사용
    // console.log(parsedToDos)
    parsedToDos.forEach(function (toDo) {
      paintToDo(toDo.text); // 상기 자바스크립트 변환 내용 중, 텍스트만 발라서 붙여넣기
    });
  }
}

function init() {
  loadToDos();
  toDoForm.addEventListener('submit', handleSubmit);
}

init();
