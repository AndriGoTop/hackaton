
document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.querySelector('.grid-container');
    setTimeout(() => gridContainer.classList.add('loaded'), 100);
    const registerModal = document.querySelector('#register-modal');
    const loginModal = document.querySelector('#login-modal');
    const switchLinks = document.querySelectorAll('.switch-link');
    const loginBtn = document.querySelector('.login-icon'); // Перемещено выше
    const authClose = document.querySelector('.auth-close');

    // Убрано дублирование обработчика
    loginBtn.addEventListener('click', () => {
        loginModal.classList.add('show');
    });

    setupInfiniteScroll();
    
    document.querySelectorAll('.scroll-item').forEach(item => {
        item.addEventListener('mouseover', () => item.style.transform = 'scale(1.05)');
        item.addEventListener('mouseout', () => item.style.transform = 'scale(1)');
    });

    // Удален дублирующийся блок кода с loginBtn

    authClose.addEventListener('click', () => {
        loginModal.classList.remove('show');
        registerModal.classList.remove('show');
    });

    window.addEventListener('click', (e) => {
        if(e.target.classList.contains('auth-modal')) {
            loginModal.classList.remove('show');
            registerModal.classList.remove('show');
        }
    });

    switchLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const currentModal = e.target.closest('.auth-modal');
            currentModal.classList.remove('show');
            
            currentModal.id === 'login-modal' 
                ? registerModal.classList.add('show')
                : loginModal.classList.add('show');
        });
    });
    
    

    // Закрытие всех модалок
    const closeModals = () => {
        registerModal.classList.remove('show');
        loginModal.classList.remove('show');
    };

    document.querySelector("#register-modal .auth-form").addEventListener("submit", async function (e) {
        e.preventDefault();
        let formData = new FormData(this);
        formData.append("register", "1"); // Важно!

        let response = await fetch("", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            }
        });

        if (response.redirected) {
            window.location.href = response.url;
        } else {
            alert("Ошибка регистрации.");
        }
});

    window.addEventListener('click', (e) => {
        if(e.target.classList.contains('auth-modal')) {
            closeModals();
        }
    });

    // Настройка фильтра
    setupFilterButton();
});

function setupInfiniteScroll() {
    const scrollTrack = document.querySelector('.infinite-scroll-track');
    const scrollItems = document.querySelectorAll('.scroll-item');
    
    function checkScrollPosition() {
        const trackWidth = scrollTrack.scrollWidth / 2;
        const trackPosition = scrollTrack.getBoundingClientRect().x;
        
        if (Math.abs(trackPosition) >= trackWidth) {
            scrollTrack.style.transition = 'none';
            scrollTrack.style.transform = 'translateX(0)';
            void scrollTrack.offsetWidth;
            scrollTrack.style.transition = 'transform linear';
        }
    }
    
    setInterval(checkScrollPosition, 1000);
    
    const originalContent = scrollTrack.innerHTML;
    scrollTrack.innerHTML = originalContent + originalContent;
}

function setupFilterButton() {
    const filterBtn = document.querySelector('.filter-btn');
    let filterPanel = null;

    function updateFilterButtonState() {
        if (!filterPanel) return;
        
        const hasCustomFilters = Array.from(filterPanel.querySelectorAll('input')).some(input => {
            if (input.type === 'checkbox') {
                const defaultState = input.id === 'filter-title' || 
                                    input.id === 'filter-author' || 
                                    input.id === 'category-science' || 
                                    input.id === 'category-tech';
                return input.checked !== defaultState;
            }
            if (input.type === 'date') return !!input.value;
            return false;
        });
        
        filterBtn.classList.toggle('active-filters', hasCustomFilters);
    }

    filterBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        
        if (!filterPanel) {
            filterPanel = document.createElement('div');
            filterPanel.className = 'filter-panel';
            filterPanel.innerHTML = `
                <div class="filter-header">
                    <span>Настройки поиска</span>
                    <button class="filter-close">×</button>
                </div>
                <div class="filter-options">
                    <div class="filter-group">
                        <div class="filter-subheader">Области поиска</div>
                        <div class="filter-option">
                            <input type="checkbox" id="filter-title" checked>
                            <label for="filter-title">Заголовки</label>
                        </div>
                        <div class="filter-option">
                            <input type="checkbox" id="filter-author" checked>
                            <label for="filter-author">Авторы</label>
                        </div>
                        <div class="filter-option">
                            <input type="checkbox" id="filter-content">
                            <label for="filter-content">Содержание</label>
                        </div>
                    </div>
                    
                    <div class="filter-group">
                        <div class="filter-subheader">Категории</div>
                        <div class="filter-option">
                            <input type="checkbox" id="category-science" checked>
                            <label for="category-science">Наука</label>
                        </div>
                        <div class="filter-option">
                            <input type="checkbox" id="category-tech" checked>
                            <label for="category-tech">Технологии</label>
                        </div>
                        <div class="filter-option">
                            <input type="checkbox" id="category-art">
                            <label for="category-art">Искусство</label>
                        </div>
                        <div class="filter-option">
                            <input type="checkbox" id="category-history">
                            <label for="category-history">История</label>
                        </div>
                    </div>
                    
                    <div class="filter-group">
                        <div class="filter-subheader">Временной период</div>
                        <div class="filter-date-range">
                            <input type="date" id="date-from" placeholder="С">
                            <span>—</span>
                            <input type="date" id="date-to" placeholder="По">
                        </div>
                    </div>
                </div>
                <div class="filter-footer">
                    <button class="filter-reset">Сбросить</button>
                    <button class="filter-apply">Применить</button>
                </div>
            `;

            const applyBtn = filterPanel.querySelector('.filter-apply');
            const resetBtn = filterPanel.querySelector('.filter-reset');
            const closeBtn = filterPanel.querySelector('.filter-close');

            applyBtn.addEventListener('click', () => {
                filterPanel.classList.remove('show');
                updateFilterButtonState();
            });

            resetBtn.addEventListener('click', () => {
                filterPanel.querySelectorAll('input').forEach(checkbox => {
                    checkbox.checked = checkbox.id.includes('category') ? 
                        (checkbox.id === 'category-science' || checkbox.id === 'category-tech') : 
                        checkbox.id !== 'filter-content';
                });
                filterPanel.querySelectorAll('input[type="date"]').forEach(input => input.value = '');
                updateFilterButtonState();
            });

            closeBtn.addEventListener('click', () => {
                filterPanel.classList.remove('show');
                updateFilterButtonState();
            });

            filterPanel.querySelectorAll('input').forEach(input => {
                input.addEventListener('change', updateFilterButtonState);
            });

            document.body.appendChild(filterPanel);
        }
        
        
        filterPanel.classList.toggle('show');
        updateFilterButtonState();
    });

    document.addEventListener('click', (e) => {
        if (filterPanel && !filterPanel.contains(e.target) && e.target !== filterBtn) {
            filterPanel.classList.remove('show');
        }
    });
}
