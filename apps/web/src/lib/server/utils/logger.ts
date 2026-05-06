import pino from 'pino';
import { env as privateEnv } from '$env/dynamic/private';

const isDevelopment = privateEnv.NODE_ENV !== 'production';

const logger = pino({
	level: privateEnv.LOG_LEVEL || (isDevelopment ? 'debug' : 'info'),
	transport: isDevelopment
		? {
				target: 'pino-pretty',
				options: {
					colorize: true,
					translateTime: 'HH:MM:ss.l',
					ignore: 'pid,hostname'
				}
			}
		: undefined
});

export interface PerformanceContext {
	operation: string;
	duration: number;
	[key: string]: unknown;
}

const SLOW_OPERATION_THRESHOLD_MS = 1000;
const SLOW_QUERY_THRESHOLD_MS = 500;
const SLOW_REQUEST_THRESHOLD_MS = 2000;

export const timeOperation = async <T>(
	operation: string,
	fn: () => Promise<T>,
	context?: Record<string, unknown>
): Promise<T> => {
	const start = performance.now();
	try {
		const result = await fn();
		const duration = performance.now() - start;
		const logContext: PerformanceContext = {
			operation,
			duration: Math.round(duration * 100) / 100,
			...(context || {})
		};

		if (duration > SLOW_OPERATION_THRESHOLD_MS) {
			logger.warn(logContext, `⚠️  Slow operation: ${operation}`);
		} else {
			logger.debug(logContext, `⏱️  ${operation}`);
		}

		return result;
	} catch (error) {
		const duration = performance.now() - start;
		logger.error(
			{
				operation,
				duration: Math.round(duration * 100) / 100,
				error: error instanceof Error ? error.message : String(error),
				...(context || {})
			},
			`❌ Failed: ${operation}`
		);
		throw error;
	}
};

export const logRequest = (
	method: string,
	path: string,
	statusCode: number,
	duration: number,
	context?: Record<string, unknown>
) => {
	const logContext = {
		type: 'request',
		method,
		path,
		statusCode,
		duration: Math.round(duration * 100) / 100,
		...(context || {})
	};

	if (duration > SLOW_REQUEST_THRESHOLD_MS) {
		logger.warn(logContext, `⚠️  Slow request: ${method} ${path}`);
	} else if (statusCode >= 400) {
		logger.error(logContext, `❌ Request error: ${method} ${path}`);
	} else {
		logger.info(logContext, `📥 ${method} ${path}`);
	}
};

export const logQuery = (
	query: string,
	duration: number,
	context?: Record<string, unknown>
) => {
	const logContext = {
		type: 'query',
		query: query.length > 100 ? query.substring(0, 100) + '...' : query,
		duration: Math.round(duration * 100) / 100,
		...(context || {})
	};

	if (duration > SLOW_QUERY_THRESHOLD_MS) {
		logger.warn(logContext, `⚠️  Slow query: ${duration}ms`);
	} else {
		logger.debug(logContext, `💾 Query executed`);
	}
};

export const logApiCall = (
	service: string,
	endpoint: string,
	method: string,
	duration: number,
	statusCode?: number,
	context?: Record<string, unknown>
) => {
	const logContext = {
		type: 'api_call',
		service,
		endpoint,
		method,
		duration: Math.round(duration * 100) / 100,
		statusCode,
		...(context || {})
	};

	if (duration > SLOW_OPERATION_THRESHOLD_MS) {
		logger.warn(logContext, `⚠️  Slow API call: ${service} ${endpoint}`);
	} else if (statusCode && statusCode >= 400) {
		logger.error(logContext, `❌ API error: ${service} ${endpoint}`);
	} else {
		logger.info(logContext, `🌐 ${service} ${endpoint}`);
	}
};

export const logHttpRequest = (
	url: string,
	method: string,
	duration: number,
	statusCode?: number,
	context?: Record<string, unknown>
) => {
	const logContext = {
		type: 'http_request',
		url,
		method,
		duration: Math.round(duration * 100) / 100,
		statusCode,
		...(context || {})
	};

	if (duration > SLOW_OPERATION_THRESHOLD_MS) {
		logger.warn(logContext, `⚠️  Slow HTTP request: ${url}`);
	} else if (statusCode && statusCode >= 400) {
		logger.error(logContext, `❌ HTTP error: ${url}`);
	} else {
		logger.debug(logContext, `📡 HTTP ${method} ${url}`);
	}
};

export default logger;
export { logger };

