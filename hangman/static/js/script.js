let letrasEscolhidas = [];
let erros = 0;

function desenharForca(erros) {
    const canvas = document.getElementById('forcaCanvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Base da forca
    ctx.fillStyle = '#000';
    ctx.fillRect(10, 230, 180, 5);
    ctx.fillRect(50, 10, 5, 220);
    ctx.fillRect(50, 10, 100, 5);
    ctx.fillRect(150, 10, 5, 30);

    // Desenho do boneco
    if (erros > 0) ctx.arc(152, 50, 20, 0, Math.PI * 2); // cabeça
    if (erros > 1) ctx.fillRect(150, 70, 5, 50); // tronco
    if (erros > 2) ctx.fillRect(130, 100, 20, 5); // braço esquerdo
    if (erros > 3) ctx.fillRect(160, 100, 20, 5); // braço direito
    if (erros > 4) ctx.fillRect(130, 130, 20, 5); // perna esquerda
    if (erros > 5) ctx.fillRect(160, 130, 20, 5); // perna direita
}

function gerarTeclado() {
    const alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const tecladoDiv = document.getElementById('teclado');
    tecladoDiv.innerHTML = ''; // Limpa o teclado antes de gerar
    alfabeto.split('').forEach(letra => {
        const botao = document.createElement('button');
        botao.innerText = letra;
        botao.onclick = () => selecionarLetra(letra);
        tecladoDiv.appendChild(botao);
    });
}

function selecionarLetra(letra) {
    letrasEscolhidas.push(letra);
    document.getElementById('letrasEscolhidas').innerText = letrasEscolhidas.join(', ');

    if (palavra.includes(letra)) {
        // Atualizar a palavra secreta se a letra estiver correta
        const palavraSecretaElement = document.getElementById('palavraSecreta');
        let novaPalavraSecreta = '';
        for (let i = 0; i < palavra.length; i++) {
            if (letrasEscolhidas.includes(palavra[i])) {
                novaPalavraSecreta += palavra[i] + ' ';
            } else {
                novaPalavraSecreta += '_ ';
            }
        }
        palavraSecretaElement.innerText = novaPalavraSecreta.trim();
    } else {
        erros++;
        desenharForca(erros);

        if (erros >= 6) {
            alert('Você perdeu! A palavra era: ' + palavra);
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
        }
    }
}

function escolherProfessor() {
    const professorId = document.getElementById('professorSelect').value;
    if (professorId) {
        fetch(`/temas_por_professor/${professorId}`)
            .then(response => response.json())
            .then(data => {
                const temaSelect = document.getElementById('temaSelect');
                temaSelect.innerHTML = '';
                data.temas.forEach(tema => {
                    const option = document.createElement('option');
                    option.value = tema.id;
                    option.text = tema.nome;
                    temaSelect.appendChild(option);
                });
                document.getElementById('temaContainer').style.display = 'block';  // Mostra o campo de tema
            })
            .catch(error => console.error('Erro ao carregar temas:', error));
    }
}
let palavra = '';
function carregarJogo() {
    const temaId = document.getElementById('temaSelect').value;
    if (temaId) {
        fetch(`/jogo_por_tema/${temaId}/`)
            .then(response => response.json())
            .then(data => {
                palavra = data.palavra ? data.palavra.toUpperCase() : '';
                if (palavra) {
                    iniciarJogo();
                } else {
                    alert('Nenhuma palavra carregada para o tema selecionado.');
                }
            });
    }
}

function iniciarJogo() {
    letrasEscolhidas = [];
    erros = 0;
    document.getElementById('letrasEscolhidas').innerText = 'Nenhuma';
    desenharForca(0);
    atualizarPalavraSecreta();
    gerarTeclado();
}
function atualizarPalavraSecreta() {
    const palavraSecretaElement = document.getElementById('palavraSecreta');
    let novaPalavraSecreta = '';
    for (let i = 0; i < palavra.length; i++) {
        if (letrasEscolhidas.includes(palavra[i])) {
            novaPalavraSecreta += palavra[i] + ' ';
        } else {
            novaPalavraSecreta += '_ ';
        }
    }
    palavraSecretaElement.innerText = novaPalavraSecreta.trim();
}
