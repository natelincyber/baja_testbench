// Simple client-side router
class Router {
    constructor() {
        this.routes = {
            '/': 'route-home',
            '/tests': 'route-tests',
            '/outputs': 'route-outputs'
        };
        this.currentRoute = '/';
        this.init();
    }

    init() {
        // Handle hash changes
        window.addEventListener('hashchange', () => this.handleRoute());
        // Handle initial load
        this.handleRoute();
    }

    handleRoute() {
        const hash = window.location.hash.slice(1) || '/';
        this.navigate(hash);
    }

    navigate(path) {
        // Update URL
        window.location.hash = path;
        this.currentRoute = path;

        // Hide all routes
        document.querySelectorAll('.route').forEach(route => {
            route.classList.remove('active');
        });

        // Show target route
        const routeId = this.routes[path];
        if (routeId) {
            const targetRoute = document.getElementById(routeId);
            if (targetRoute) {
                targetRoute.classList.add('active');
            }
        }

        // Update nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-route') === path) {
                link.classList.add('active');
            }
        });
    }
}

// Initialize router
const router = new Router();

