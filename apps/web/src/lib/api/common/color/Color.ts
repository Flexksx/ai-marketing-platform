export default class Color {
	private value: string;
	constructor(hexValue: string) {
		this.value = hexValue;
	}
	static fromHex(hex: string): Color {
		return new Color(hex);
	}

	static fromRGB({ red, green, blue }: { red: number; green: number; blue: number }): Color {
		const hex = `#${((1 << 24) + (red << 16) + (green << 8) + blue).toString(16).slice(1)}`;
		return new Color(hex);
	}
	toHex(): string {
		return this.value;
	}
	toRgb(): string {
		const hex = this.value.replace('#', '');
		const bigint = parseInt(hex, 16);
		const red = (bigint >> 16) & 255;
		const green = (bigint >> 8) & 255;
		const blue = bigint & 255;
		return `rgb(${red}, ${green}, ${blue})`;
	}
}
