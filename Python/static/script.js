document.addEventListener("DOMContentLoaded", () => {
    // 1. Xử lý click cho các thẻ Card
    const cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.addEventListener("click", function() {
            // Lấy đường dẫn từ thuộc tính data-url
            const url = this.getAttribute("data-url");
            if (url) {
                window.location.href = url;
            }
        });
    });

    // 2. Xử lý sự kiện Settings
    const settingsBtn = document.getElementById("settingsBtn");
    const settingsMenu = document.getElementById("settingsMenu");
    const brightnessBtn = document.getElementById("brightnessBtn");
    const brightnessControl = document.getElementById("brightnessControl");
    const slider = document.getElementById("brightnessSlider");
    const exitBtn = document.getElementById("exitBtn");

    if (settingsBtn) {
        settingsBtn.onclick = () => {
            settingsMenu.classList.toggle("hidden");
        };
    }

    if (brightnessBtn) {
        brightnessBtn.onclick = () => {
            brightnessControl.classList.toggle("hidden");
        };
    }

    if (slider) {
        // Cập nhật độ sáng ngay khi kéo (dùng thẻ document.documentElement thay vì body để áp dụng tốt hơn)
        slider.oninput = () => {
            document.documentElement.style.filter = `brightness(${slider.value}%)`;
        };
    }

    if (exitBtn) {
        exitBtn.onclick = () => {
            if (confirm("Bạn có chắc chắn muốn thoát?")) {
                window.close();
            }
        };
    }
});