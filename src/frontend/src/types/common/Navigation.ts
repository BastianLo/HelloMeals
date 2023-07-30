export class Navigation {
    count: number | null;
    start: number | null;
    end: number | null;
    next: string | null;
    previous: string | null;

    constructor(data: Partial<Navigation> = {}) {
        this.count = data.count || null;
        this.start = data.start || null;
        this.end = data.end || null;
        this.next = data.next || null;
        this.previous = data.previous || null;
    }
}
