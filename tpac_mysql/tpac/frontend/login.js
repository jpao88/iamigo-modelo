const formulario = document.getElementById("form-login");
const campoNome = document.getElementById("nome");
const campoSenha = document.getElementById("senha");
const botao = document.getElementById("botao-entrar");
const mensagem = document.getElementById("mensagem");

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  mensagem.textContent = "";
  mensagem.className = "mensagem";
  botao.disabled = true;
  botao.textContent = "Entrando...";

  try {
    const resposta = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nome: campoNome.value.trim(),
        senha: campoSenha.value
      })
    });

    const corpo = await resposta.json();

    if (!resposta.ok) {
      const texto = typeof corpo.detail === "string"
        ? corpo.detail
        : "Preencha nome e senha.";
      mostrarErro(texto);
      return;
    }

    sessionStorage.setItem("token", corpo.dados.access_token);
    sessionStorage.setItem("usuario", JSON.stringify(corpo.dados.usuario));

    window.location.href = "painel.html";
  } catch (erro) {
    console.error("Falha no login:", erro);
    mostrarErro("Não foi possível conectar ao servidor. A API está rodando?");
  } finally {
    botao.disabled = false;
    botao.textContent = "Entrar";
  }
});

function mostrarErro(texto) {
  mensagem.textContent = texto;
  mensagem.className = "mensagem erro";
}