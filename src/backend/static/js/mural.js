document.addEventListener('DOMContentLoaded', async function () {
    const searchBtn = document.getElementById('search-btn');
    const gameContainer = document.getElementById('gameContainer');

    searchBtn.addEventListener('click', async function () {
        const searchInput = document.getElementById('searchInput').value.trim();

        if (!searchInput) {
            alert('Por favor, insira um termo de pesquisa válido.');
            return;
        }

        try {
            const response = await fetch(`https://api.rawg.io/api/games?key=94a728c53f63486e98e4a6a65385649d&search=${searchInput}`);
            
            if (!response.ok) {
                throw new Error(`Erro na solicitação da API. Código de status: ${response.status}`);
            }

            const data = await response.json();

            gameContainer.innerHTML = ''; // Limpar o conteúdo anterior

            // Cria e adiciona cards para cada resultado
            data.results.forEach(result => {
                const card = document.createElement('div');
                card.className = 'game-card card';

                // Verifica se a descrição está definida
                const description = result.description_raw ? result.description_raw : 'Descrição não disponível';

                card.innerHTML = `
                    <div class="game-card__media" style="background-image: url('${result.background_image}');" onclick="playVideo('${result.slug}')"></div>
                    <div class="game-card__info">
                        <h3 class="game-card__name"><a href="/games/${result.slug}">${result.name}</a></h3>
                    </div>
                `;

                gameContainer.appendChild(card);
            });
        } catch (error) {
            console.error('Erro ao obter dados da API:', error);
            console.error('Detalhes do erro:', error.message);
            alert('Erro ao obter dados da API. Consulte o console para obter mais detalhes.');
        }
    });

    // Função para redirecionar para a página de detalhes do jogo
    function playVideo(slug) {
        // Redireciona para a página de detalhes do jogo com base no slug
        window.location.href = `/games/${slug}`;
    }
});