import { redirect } from '@sveltejs/kit';
import { createCategory } from '$lib/apis/categories';

export const actions = {
	default: async ({ request, locals }) => {
		const formData = await request.formData();
		const name = formData.get('name');
		const type = formData.get('type');
		const icon = formData.get('icon');

		try {
			await createCategory(locals.token, name, type, icon);
			throw redirect(303, '/categories');
		} catch (error) {
			return { error: 'Failed to create category' };
		}
	}
}; 