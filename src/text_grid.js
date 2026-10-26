

export class TextGrid {

    constructor(width, height, containerId, defChar = '█', defColor = '#000000') {

        this.width = width;
        this.height = height;
        this.defChar = defChar;
        this.defColor = defColor;

        this.textGridContainer = document.getElementById(containerId);

        this.size = width * height;

        this.charBuffer = new Array(this.size).fill(defChar);
        this.colorBuffer = new Array(this.size).fill(defColor);

        this.domCache = new Array(this.size);

        this.init();

    }


    init() {

        this.textGridContainer.innerHTML = '';

        this.textGridContainer.style.setProperty('--grid-cols', this.width);
        this.textGridContainer.style.setProperty('--grid-rows', this.height);
        this.textGridContainer.style.setProperty('--grid-max-dim', Math.max(this.width, this.height));

        const fragment = document.createDocumentFragment();

        for (let i = 0; i < this.size; i++) {
            const cell = document.createElement('span');
            cell.textContent = this.charBuffer[i];
            cell.style.color = this.colorBuffer[i];

            this.domCache[i] = cell;
            fragment.appendChild(cell);
        }

        this.textGridContainer.appendChild(fragment);
    }


    checkXY(x, y) { return x >= 0 && x < this.width && y >= 0 && y < this.height; }


    set(x, y, char, color = '#ffffff') {
        if (!this.checkXY(x, y)) { return; }
        const idx = y * this.width + x;
        this.charBuffer[idx] = char.charAt(0);
        this.colorBuffer[idx] = color;
    }


    get(x, y) {
        if (!this.checkXY(x, y)) { return null; }
        const idx = y * this.width + x;
        return {
            char: this.charBuffer[idx], 
            color: this.colorBuffer[idx]
        };
    }


    clear() {
        this.charBuffer.fill(this.defChar);
        this.colorBuffer.fill(this.defColor);
    }


    render() {
        for (let i = 0; i < this.size; i++) {
            const cell = this.domCache[i];
            // Only manipulate elements w/ changed state.
            if (cell.textContent !== this.charBuffer[i]) { cell.textContent = this.charBuffer[i]; }
            if (cell.style.color != this.colorBuffer[i]) { cell.style.color = this.colorBuffer[i]; }
        }
    }
}