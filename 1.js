
    document.addEventListener('DOMContentLoaded', function () {
        const truck = {
            length: {{ truck.length }},
            width: {{ truck.width }}
        };

        const pallets = {{ pallets | tojson }};
        const topView = document.getElementById('truck-top-view');

        const truckWidthInPixels = truck.width * 2.54;
        const truckLengthInPixels = truck.length * 2.54;
        topView.style.width = truckWidthInPixels + 'px';
        topView.style.height = truckLengthInPixels + 'px';

        let rowHeight = 0;
        const placedPallets = [];

        // Функція перевірки на накладання палет
        function isOverlapping(newPalletX, newPalletY, newPalletWidth, newPalletHeight) {
            return placedPallets.some(p => {
                return (
                    newPalletX < p.x + p.width &&
                    newPalletX + newPalletWidth > p.x &&
                    newPalletY < p.y + p.height &&
                    newPalletY + newPalletHeight > p.y
                );
            });
        }

        // Функція пошуку найближчого доступного місця для розміщення палети
        function findClosestSpace(palletWidth, palletHeight) {
            for (let y = 0; y <= truckLengthInPixels - palletHeight; y++) {
                for (let x = 0; x <= truckWidthInPixels - palletWidth; x++) {
                    if (!isOverlapping(x, y, palletWidth, palletHeight)) {
                        return { x, y };
                    }
                }
            }
            return null;
        }

        pallets.forEach((pallet, index) => {
            const palletDiv = document.createElement('div');
            const palletWidth = (pallet.width_unit === 'cm' ? pallet.width : pallet.width * 2.54);
            const palletHeight = (pallet.length_unit === 'cm' ? pallet.length : pallet.length * 2.54);

            // Знайдемо найближче доступне місце для цієї палети
            let closestSpace = findClosestSpace(palletWidth, palletHeight);

            if (closestSpace) {
                let { x, y } = closestSpace;

                // Стилі для палет
                palletDiv.style.position = 'absolute';
                palletDiv.style.border = '1px solid #000';
                palletDiv.style.width = palletWidth + 'px';
                palletDiv.style.height = palletHeight + 'px';
                palletDiv.style.left = x + 'px';
                palletDiv.style.top = y + 'px';
                palletDiv.textContent = (index + 1);

                // Записуємо позиції палети
                placedPallets.push({ x, y, width: palletWidth, height: palletHeight });

                rowHeight = Math.max(rowHeight, palletHeight);

                const truckRight = truckWidthInPixels;
                const truckBottom = truckLengthInPixels;

                if (x + palletWidth <= truckRight && y + palletHeight <= truckBottom) {
                    palletDiv.className = 'pallet pallet-inside';
                } else {
                    palletDiv.className = 'pallet pallet-outside';
                }

                topView.appendChild(palletDiv);
            } else {
                console.error("Не вдалося знайти місце для палети " + (index + 1));
            }
        });
    });