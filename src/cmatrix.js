
export class Cmatrix {
    
    constructor(
        parentSelector, 
        width, height, 
        defaultChar = ' ', 
        defaultColor = '#000'
    ) {
        this.parentContainer = document.querySelector(parentSelector);
        this.width = width;
        this.height = height;
        this.defaultChar = defaultChar;
        this.defaultColor = defaultColor;

        this.size = width * height;
        this.aspectRatio = width / height;

        this.charBuffer = new Array(this.size).fill(defaultChar);
        this.colorBuffer = new Array(this.size).fill(defaultColor);
        this.domCache = new Array(this.size);

        this.buildDOM()
        this.startResizeObserver()
    }


    buildDOM() {
        this.cmatrixWrapper = document.createElement('div');
        this.cmatrixWrapper.className = 'cmatrix-wrapper';

        this.cmatrix = document.createElement('div');
        this.cmatrix.className = 'cmatrix';
        this.cmatrix.style.gridTemplateColumns = `repeat(${this.width}, 1fr)`;
        this.cmatrix.style.gridTemplateRows = `repeat(${this.height}, 1fr)`;

        const fragment = document.createDocumentFragment();

        for (let i = 0; i < this.size; i++) {
            const cell = document.createElement('span');
            cell.textContent = this.charBuffer[i];
            cell.style.color = this.colorBuffer[i];
            this.domCache[i] = cell;
            fragment.appendChild(cell);
        }

        this.cmatrix.appendChild(fragment);
        this.cmatrixWrapper.appendChild(this.cmatrix);
        this.parentContainer.appendChild(this.cmatrixWrapper);
    }


    startResizeObserver() {
        this.resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) {
                const { width, height } = entry.contentRect;
                this.resizeToFit(width, height);
            }
        });
        this.resizeObserver.observe(this.parentContainer);
    }


    resizeToFit(parentWidthPx, parentHeightPx) {
        let targetWidthPx, targetHeightPx;
        const parentAspectRatio = parentWidthPx / parentHeightPx;

        // Container is wider
        if (parentAspectRatio > this.aspectRatio) {
            targetHeightPx = parentHeightPx;
            targetWidthPx = targetHeightPx * this.aspectRatio;
        }
        // Container is taller 
        else {
            targetWidthPx = parentWidthPx;
            targetHeightPx = targetWidthPx / this.aspectRatio;
        }

        this.cmatrixWrapper.style.width = `${targetWidthPx}px`;
        this.cmatrixWrapper.style.height = `${targetHeightPx}px`;

        const cellSizePx = targetWidthPx / this.width;
        this.cmatrix.style.fontSize = `${cellSizePx}px`;
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
        this.charBuffer.fill(this.defaultChar);
        this.colorBuffer.fill(this.defaultColor);
    }

    render() {
        for (let i = 0; i < this.size; i++) {
            const cell = this.domCache[i];
            // Only manipulate elements w/ changed state.
            if (cell.textContent !== this.charBuffer[i]) { cell.textContent = this.charBuffer[i]; }
            if (cell.style.color !== this.colorBuffer[i]) { cell.style.color = this.colorBuffer[i]; }
        }
    }


    destroy() {
        this.resizeObserver.disconnect();
        this.cmatrixWrapper.remove();
    }
}