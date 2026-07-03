// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash');
    
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            flash.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                flash.remove();
            }, 300);
        }, 4000);
    });
});

// Confirm deletion
function confirmDelete(nim) {
    return confirm(`Apakah Anda yakin ingin menghapus data mahasiswa dengan NIM ${nim}?`);
}
