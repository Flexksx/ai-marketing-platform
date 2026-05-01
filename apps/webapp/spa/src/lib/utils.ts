import { type ClassValue, clsx } from 'clsx';
import { customAlphabet } from 'nanoid';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

const ID_ALPHABET = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
const DEFAULT_ID_LENGTH = 12;
const defaultIdGenerator = customAlphabet(ID_ALPHABET, DEFAULT_ID_LENGTH);

export function newId(length = DEFAULT_ID_LENGTH) {
	if (!Number.isInteger(length) || length <= 0) {
		throw new Error('length must be a positive integer');
	}

	if (length === DEFAULT_ID_LENGTH) {
		return defaultIdGenerator();
	}

	return customAlphabet(ID_ALPHABET, length)();
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChild<T> = T extends { child?: any } ? Omit<T, 'child'> : T;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChildren<T> = T extends { children?: any } ? Omit<T, 'children'> : T;
export type WithoutChildrenOrChild<T> = WithoutChildren<WithoutChild<T>>;
export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & {
	ref?: U | null;
};
