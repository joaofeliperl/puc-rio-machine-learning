document.addEventListener('DOMContentLoaded', async function () {
    var gameSlug = '{{ game_slug }}';

    if (gameSlug) {
        try {
            const response = await fetch(`/get_game_data_by_slug/${gameSlug}`);
            if (!response.ok) {
                throw new Error(`Erro ao obter dados do jogo. Código de status: ${response.status}`);
            }

            const gameData = await response.json();

            document.querySelector('.game-details img').src = gameData.background_image;
            document.querySelector('.game-details h2').textContent = gameData.name;
            document.querySelector('.game-details p').textContent = `Sobre o jogo: ${gameData.description_raw}`;

        } catch (error) {
            console.error('Erro ao obter dados do jogo:', error);
            console.error('Detalhes do erro:', error.message);
            alert('Erro ao obter dados do jogo. Consulte o console para obter mais detalhes.');
        }
    }
});

$(document).ready(function () {
    $("#gameRating").rateYo({
        rating: 0,
        fullStar: true,
        numStars: 5,
        onChange: function (rating, rateYoInstance) {
            $("#gameRatingValue").val(rating);
        }
    });
});