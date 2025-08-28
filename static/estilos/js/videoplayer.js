document.addEventListener('DOMContentLoaded', (event) => {
    const videos = document.querySelectorAll('.video-item');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    let currentVideoIndex = 0;

    function showVideo(index) {
        videos.forEach((video, i) => {
            if (i === index) {
                video.style.display = 'block';
                // Reproducir automáticamente el video al mostrarlo
                if (video.tagName === 'VIDEO') {
                    video.play();
                }
            } else {
                video.style.display = 'none';
                // Pausar el video que se oculta
                if (video.tagName === 'VIDEO') {
                    video.pause();
                }
            }
        });
    }

    // Función para ir al siguiente video
    nextBtn.addEventListener('click', () => {
        currentVideoIndex = (currentVideoIndex + 1) % videos.length;
        showVideo(currentVideoIndex);
    });

    // Función para ir al video anterior
    prevBtn.addEventListener('click', () => {
        currentVideoIndex = (currentVideoIndex - 1 + videos.length) % videos.length;
        showVideo(currentVideoIndex);
    });

    // Evento para pasar al siguiente video cuando el actual termina
    videos.forEach(video => {
        video.addEventListener('ended', () => {
            currentVideoIndex = (currentVideoIndex + 1) % videos.length;
            showVideo(currentVideoIndex);
        });
    });

    // Mostrar el primer video al cargar la página
    if (videos.length > 0) {
        showVideo(currentVideoIndex);
    }
});
