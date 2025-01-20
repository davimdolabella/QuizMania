const controls = document.querySelectorAll('.scroll-button'); // Botões de controle
let current_quiz = 4; // Começa no índice 4
const quizes = document.querySelectorAll('.quiz-single'); // Lista de quizzes
const maxItems = quizes.length;

// Marca o item inicial como "ativo"
quizes[current_quiz].classList.add('current-item');
quizes[current_quiz].scrollIntoView({
  inline: "center",
  behavior: "smooth",
});

// Adiciona evento de clique aos botões
controls.forEach(control => {
  control.addEventListener('click', () => {
    const isLeft = control.classList.contains('scroll-left'); // Verifica se o botão é para a esquerda

    // Atualiza o índice com rotação circular
    if (isLeft) {
      current_quiz = (current_quiz - 1 + maxItems) % maxItems;
    } else {
      current_quiz = (current_quiz + 1) % maxItems;
    }

    // Remove a classe de todos os itens e atualiza o atual
    quizes.forEach(quiz => quiz.classList.remove('current-item'));
    quizes[current_quiz].classList.add('current-item');

    // Centraliza o item atual
    quizes[current_quiz].scrollIntoView({
      inline: "center",
      behavior: "smooth",
    });
  });
});

// Adiciona evento de clique para cada quiz
quizes.forEach(quiz => {
  quiz.addEventListener('click', () => {
    alert('kmd'); // Ação ao clicar em um quiz
  });
});
