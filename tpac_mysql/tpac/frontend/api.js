const API_URL = "http://127.0.0.1:8000";

function obterToken() {
  return sessionStorage.getItem("token");
}

function obterUsuario() {
  const texto = sessionStorage.getItem("usuario");
  return texto ? JSON.parse(texto) : null;
}

function limparSessao() {
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("usuario");
}

async function requisicaoAutenticada(caminho, opcoes = {}) {
  const resposta = await fetch(`${API_URL}${caminho}`, {
    ...opcoes,
    headers: {
      ...(opcoes.headers || {}),
      Authorization: `Bearer ${obterToken()}`
    }
  });

  if (resposta.status === 401) {
    limparSessao();
    window.location.href = "index.html";
    return null;
  }

  return resposta;
}