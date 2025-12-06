// Funcionalidad de búsqueda y filtrado de hoteles
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search-input');
    const precioSelect = document.querySelectorAll('.filter-select')[0];
    const estrellasSelect = document.querySelectorAll('.filter-select')[1];
    const btnSearch = document.querySelector('.btn-search');
    const hotelCards = document.querySelectorAll('.hotel-card');

    // Si no hay elementos, salir
    if (!searchInput || !btnSearch || hotelCards.length === 0) return;

    // Función para filtrar hoteles
    function filtrarHoteles() {
        const buscar = searchInput.value.toLowerCase().trim();
        const precioFiltro = precioSelect.value;
        const estrellasFiltro = estrellasSelect.value;

        let hotelesVisibles = Array.from(hotelCards);

        // Filtrar por nombre
        if (buscar) {
            hotelesVisibles = hotelesVisibles.filter(card => {
                const nombre = card.querySelector('.hotel-name').textContent.toLowerCase();
                return nombre.includes(buscar);
            });
        }

        // Filtrar por estrellas
        if (estrellasFiltro) {
            hotelesVisibles = hotelesVisibles.filter(card => {
                const estrellas = card.querySelectorAll('.star:not(.empty)').length;
                return estrellas == parseInt(estrellasFiltro);
            });
        }

        // Ordenar por precio
        if (precioFiltro) {
            hotelesVisibles.sort((a, b) => {
                const precioA = parseInt(a.querySelector('.price-value').textContent.replace(/[^0-9]/g, ''));
                const precioB = parseInt(b.querySelector('.price-value').textContent.replace(/[^0-9]/g, ''));
                return precioFiltro === 'low' ? precioA - precioB : precioB - precioA;
            });
        }

        // Ocultar todos los hoteles
        hotelCards.forEach(card => card.style.display = 'none');

        // Mostrar solo los filtrados
        hotelesVisibles.forEach(card => card.style.display = 'block');

        if (precioFiltro && hotelesVisibles.length > 0) {
            const grid = document.querySelector('.hotel-grid');
            hotelesVisibles.forEach(card => grid.appendChild(card));
        }

        // Mostrar mensaje si no hay resultados
        const grid = document.querySelector('.hotel-grid');
        const oldNoResults = grid.querySelector('.no-results');

        if (hotelesVisibles.length === 0) {
            if (!oldNoResults) {
                const noResults = document.createElement('div');
                noResults.className = 'no-results';
                noResults.style.cssText = 'grid-column: 1 / -1; text-align: center; padding: 60px 20px;';
                noResults.innerHTML = `
                    <i class="fas fa-search" style="font-size: 64px; color: #DDD; margin-bottom: 20px;"></i>
                    <h3 style="color: #999;">No se encontraron hoteles</h3>
                    <p style="color: #666; margin-top: 10px;">Intenta con otros filtros de búsqueda</p>
                `;
                grid.appendChild(noResults);
            }
        } else {
            // Eliminar mensaje de no resultados si existe
            if (oldNoResults) oldNoResults.remove();
        }

        // Mostrar contador de resultados
        console.log(`Mostrando ${hotelesVisibles.length} de ${hotelCards.length} hoteles`);
    }

    // Eventos
    btnSearch.addEventListener('click', function (e) {
        e.preventDefault();
        filtrarHoteles();
    });

    searchInput.addEventListener('keyup', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            filtrarHoteles();
        }
    });

    precioSelect.addEventListener('change', filtrarHoteles);
    estrellasSelect.addEventListener('change', filtrarHoteles);

    // Búsqueda en tiempo real mientras escribes (opcional)
    let searchTimeout;
    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(filtrarHoteles, 300); // Espera 300ms después de dejar de escribir
    });
});
