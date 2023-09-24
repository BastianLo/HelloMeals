export class Nutrients {
    energyKj: number | null;
    energyKcal: number | null;
    fat: number | null;
    fatSaturated: number | null;
    carbs: number | null;
    sugar: number | null;
    protein: number | null;
    salt: number | null;

    constructor(data: Partial<Nutrients> = {}) {
        this.energyKj = data.energyKj || null;
        this.energyKcal = data.energyKcal || null;
        this.fat = data.fat || null;
        this.fatSaturated = data.fatSaturated || null;
        this.carbs = data.carbs || null;
        this.sugar = data.sugar || null;
        this.protein = data.protein || null;
        this.salt = data.salt || null;
    }
}
