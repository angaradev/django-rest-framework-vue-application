const app = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    data: {
        message: 'Hello World',
        url: '/supplier/'
    },
    methods: {
        goToUrl(event) {
            let url = event.currentTarget.getAttribute('data-href');
            window.location.href = url
            //window.location.href = this.url + pk + '/';
        }
    }
});