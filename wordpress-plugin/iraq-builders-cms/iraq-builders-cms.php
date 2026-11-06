<?php
/**
 * Plugin Name: Iraq Builders CMS
 * Description: لوحة بسيطة لإدارة أخبار وأنشطة ومعلومات التبرع لموقع منظمة بناة العراق، مع واجهة قراءة عامة (REST) للموقع الثابت.
 * Version: 1.1.0
 * Author: Iraq Builders
 * License: GPL-2.0-or-later
 * Text Domain: ibcms
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'IBCMS_VERSION', '1.1.0' );
define( 'IBCMS_NS', 'ib/v1' );

/* ------------------------------------------------------------------
 * الإعدادات
 * ------------------------------------------------------------------ */

/** النطاقات المسموح لها بقراءة الواجهة العامة من المتصفح (CORS). */
function ibcms_allowed_origins() {
	$defaults = array(
		'https://iraqbuilders.org',
		'https://www.iraqbuilders.org',
		'https://ibmedical9-ops.github.io',
	);
	return (array) apply_filters( 'ibcms_allowed_origins', $defaults );
}

/** أيقونات الأنشطة المتاحة عند غياب الصورة. */
function ibcms_icons() {
	return array(
		''      => 'بدون أيقونة',
		'cross' => 'طبي',
		'shirt' => 'ملابس',
		'tools' => 'مشاريع وأعمال',
		'moon'  => 'رمضان',
		'heart' => 'كفالة ورعاية',
		'gift'  => 'مساعدات',
	);
}

/** أماكن عرض النشاط في صفحة الأنشطة. */
function ibcms_groups() {
	return array(
		'general' => 'ضمن قائمة الأنشطة',
		'ramadan' => 'ضمن قسم «أنشطة رمضان»',
		'project' => 'مشروع مميز (قسم خاص، مثل مشروع خطوة)',
	);
}

/* ------------------------------------------------------------------
 * أنواع المحتوى: الأخبار والأنشطة
 * ------------------------------------------------------------------ */

function ibcms_cpt_args( $singular, $plural, $cap_singular, $cap_plural, $icon, $title_here ) {
	return array(
		'labels'          => array(
			'name'               => $plural,
			'singular_name'      => $singular,
			'add_new'            => 'إضافة جديد',
			'add_new_item'       => 'إضافة ' . $singular,
			'edit_item'          => 'تعديل ' . $singular,
			'new_item'           => $singular . ' جديد',
			'view_item'          => 'عرض',
			'search_items'       => 'بحث',
			'not_found'          => 'لا يوجد شيء بعد',
			'not_found_in_trash' => 'سلة المحذوفات فارغة',
			'all_items'          => 'كل ' . $plural,
			'menu_name'          => $plural,
			'featured_image'     => 'الصورة',
			'set_featured_image' => 'اختيار صورة',
			'remove_featured_image' => 'إزالة الصورة',
			'use_featured_image' => 'استخدام كصورة',
		),
		'public'              => false,
		'show_ui'             => true,
		'show_in_menu'        => true,
		'show_in_rest'        => false, // يعطّل محرر Gutenberg المعقد لهذا النوع
		'exclude_from_search' => true,
		'publicly_queryable'  => false,
		'has_archive'         => false,
		'rewrite'             => false,
		'menu_icon'           => $icon,
		'supports'            => array( 'title', 'thumbnail' ),
		'capability_type'     => array( $cap_singular, $cap_plural ),
		'map_meta_cap'        => true,
	);
}

add_action( 'init', function () {
	register_post_type( 'ib_news', array_merge(
		ibcms_cpt_args( 'خبر', 'الأخبار', 'ibnews', 'ibnews_items', 'dashicons-megaphone', '' ),
		array( 'menu_position' => 3 )
	) );
	register_post_type( 'ib_activity', array_merge(
		ibcms_cpt_args( 'نشاط', 'الأنشطة', 'ibactivity', 'ibactivity_items', 'dashicons-heart', '' ),
		array( 'menu_position' => 4 )
	) );
} );

add_filter( 'enter_title_here', function ( $text, $post ) {
	if ( $post && 'ib_news' === $post->post_type ) {
		return 'عنوان الخبر (بالعربية)';
	}
	if ( $post && 'ib_activity' === $post->post_type ) {
		return 'اسم النشاط (بالعربية)';
	}
	return $text;
}, 10, 2 );

/** تسمية صندوق الصورة. */
add_action( 'add_meta_boxes', function () {
	foreach ( array( 'ib_news' => 'صورة الخبر', 'ib_activity' => 'صورة النشاط' ) as $type => $label ) {
		remove_meta_box( 'postimagediv', $type, 'side' );
		add_meta_box( 'postimagediv', $label, 'post_thumbnail_meta_box', $type, 'side', 'default' );
	}
}, 5 );

/* ------------------------------------------------------------------
 * حقول المحتوى
 * ------------------------------------------------------------------ */

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'ibcms_fields', 'المحتوى', 'ibcms_render_fields', array( 'ib_news', 'ib_activity' ), 'normal', 'high' );
} );

function ibcms_render_fields( $post ) {
	wp_nonce_field( 'ibcms_save_' . $post->ID, 'ibcms_nonce' );
	$m = function ( $k ) use ( $post ) {
		return get_post_meta( $post->ID, $k, true );
	};
	$is_news = 'ib_news' === $post->post_type;
	?>
	<style>
		.ibcms label{display:block;font-weight:600;margin:14px 0 6px}
		.ibcms input[type=text],.ibcms input[type=url],.ibcms input[type=number],.ibcms select,.ibcms textarea{width:100%;max-width:100%;font-size:15px}
		.ibcms textarea{min-height:170px;line-height:1.8}
		.ibcms .en{direction:ltr;text-align:left}
		.ibcms .hint{color:#646970;font-size:13px;margin:4px 0 0}
		.ibcms h4{margin:22px 0 0;padding-top:14px;border-top:1px solid #dcdcde}
	</style>
	<div class="ibcms">
		<label for="ib_text_ar"><?php echo $is_news ? 'نص الخبر (بالعربية)' : 'وصف النشاط (بالعربية)'; ?></label>
		<textarea id="ib_text_ar" name="ib_text_ar" dir="rtl"><?php echo esc_textarea( $m( '_ib_text_ar' ) ); ?></textarea>
		<p class="hint">اكتب فقرات عادية. اترك سطرًا فارغًا بين الفقرة والأخرى.</p>

		<h4>النسخة الإنجليزية (اختياري)</h4>
		<label for="ib_title_en"><?php echo $is_news ? 'News title' : 'Activity name'; ?></label>
		<input type="text" id="ib_title_en" name="ib_title_en" class="en" dir="ltr" value="<?php echo esc_attr( $m( '_ib_title_en' ) ); ?>">
		<label for="ib_text_en"><?php echo $is_news ? 'News text' : 'Description'; ?></label>
		<textarea id="ib_text_en" name="ib_text_en" class="en" dir="ltr"><?php echo esc_textarea( $m( '_ib_text_en' ) ); ?></textarea>

		<?php if ( $is_news ) : ?>
			<h4>رابط (اختياري)</h4>
			<label for="ib_link">رابط المنشور الأصلي على فيسبوك أو غيره</label>
			<input type="url" id="ib_link" name="ib_link" class="en" dir="ltr" placeholder="https://" value="<?php echo esc_attr( $m( '_ib_link' ) ); ?>">
		<?php else : ?>
			<h4>العرض في الموقع</h4>
			<label for="ib_group">مكان العرض في صفحة الأنشطة</label>
			<select id="ib_group" name="ib_group">
				<?php $cur_group = $m( '_ib_group' ) ? $m( '_ib_group' ) : 'general'; ?>
				<?php foreach ( ibcms_groups() as $k => $label ) : ?>
					<option value="<?php echo esc_attr( $k ); ?>" <?php selected( $cur_group, $k ); ?>><?php echo esc_html( $label ); ?></option>
				<?php endforeach; ?>
			</select>
			<label for="ib_order">الترتيب (الرقم الأصغر يظهر أولًا)</label>
			<input type="number" id="ib_order" name="ib_order" min="0" max="999" value="<?php echo esc_attr( $m( '_ib_order' ) !== '' ? $m( '_ib_order' ) : 50 ); ?>">
			<label for="ib_icon">أيقونة (تظهر إذا لم تضع صورة)</label>
			<select id="ib_icon" name="ib_icon">
				<?php foreach ( ibcms_icons() as $k => $label ) : ?>
					<option value="<?php echo esc_attr( $k ); ?>" <?php selected( $m( '_ib_icon' ), $k ); ?>><?php echo esc_html( $label ); ?></option>
				<?php endforeach; ?>
			</select>
			<label><input type="checkbox" name="ib_featured" value="1" <?php checked( $m( '_ib_featured' ), '1' ); ?>> يظهر في الصفحة الرئيسية</label>
		<?php endif; ?>
	</div>
	<?php
}

add_action( 'save_post', function ( $post_id, $post ) {
	if ( ! in_array( $post->post_type, array( 'ib_news', 'ib_activity' ), true ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! isset( $_POST['ibcms_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['ibcms_nonce'] ) ), 'ibcms_save_' . $post_id ) ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}
	$txt = function ( $key, $max ) {
		$v = isset( $_POST[ $key ] ) ? sanitize_textarea_field( wp_unslash( $_POST[ $key ] ) ) : '';
		return function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
	};
	$line = function ( $key, $max ) {
		$v = isset( $_POST[ $key ] ) ? sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) : '';
		return function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
	};
	update_post_meta( $post_id, '_ib_text_ar', $txt( 'ib_text_ar', 20000 ) );
	update_post_meta( $post_id, '_ib_text_en', $txt( 'ib_text_en', 20000 ) );
	update_post_meta( $post_id, '_ib_title_en', $line( 'ib_title_en', 200 ) );
	if ( 'ib_news' === $post->post_type ) {
		$link = isset( $_POST['ib_link'] ) ? esc_url_raw( wp_unslash( $_POST['ib_link'] ), array( 'http', 'https' ) ) : '';
		update_post_meta( $post_id, '_ib_link', $link );
	} else {
		$order = isset( $_POST['ib_order'] ) ? max( 0, min( 999, (int) $_POST['ib_order'] ) ) : 50;
		update_post_meta( $post_id, '_ib_order', $order );
		$icon = isset( $_POST['ib_icon'] ) ? sanitize_key( wp_unslash( $_POST['ib_icon'] ) ) : '';
		update_post_meta( $post_id, '_ib_icon', array_key_exists( $icon, ibcms_icons() ) ? $icon : '' );
		update_post_meta( $post_id, '_ib_featured', ! empty( $_POST['ib_featured'] ) ? '1' : '0' );
		$group = isset( $_POST['ib_group'] ) ? sanitize_key( wp_unslash( $_POST['ib_group'] ) ) : 'general';
		update_post_meta( $post_id, '_ib_group', array_key_exists( $group, ibcms_groups() ) ? $group : 'general' );
	}
}, 10, 2 );

/* ------------------------------------------------------------------
 * معلومات التبرع
 * ------------------------------------------------------------------ */

function ibcms_donation_defaults() {
	return array(
		'methods' => array(
			array( 'ar' => 'ماستر كارد (الرافدين)', 'en' => 'Mastercard (Al-Rafidain)', 'number' => '6173766863' ),
			array( 'ar' => 'زين كاش', 'en' => 'Zain Cash', 'number' => '07815109866' ),
		),
		'note_ar' => 'يرجى ذكر اسمكم ورقم هاتفكم في ملاحظات التحويل في حال رغبتكم بالحصول على وصل لتبرعكم الكريم.',
		'note_en' => 'Please mention your name and phone number in the transfer notes if you would like a receipt for your generous donation.',
	);
}

function ibcms_get_donation() {
	$d = get_option( 'ib_donation' );
	if ( ! is_array( $d ) || empty( $d['methods'] ) ) {
		$d = ibcms_donation_defaults();
	}
	return $d;
}

add_action( 'admin_menu', function () {
	add_menu_page( 'معلومات التبرع', 'معلومات التبرع', 'ibcms_edit_donation', 'ibcms-donation', 'ibcms_render_donation', 'dashicons-money-alt', 5 );
} );

function ibcms_render_donation() {
	if ( ! current_user_can( 'ibcms_edit_donation' ) ) {
		wp_die( 'غير مسموح.' );
	}
	$d       = ibcms_get_donation();
	$methods = $d['methods'];
	while ( count( $methods ) < 5 ) {
		$methods[] = array( 'ar' => '', 'en' => '', 'number' => '' );
	}
	?>
	<div class="wrap" dir="rtl">
		<h1>معلومات التبرع</h1>
		<?php if ( isset( $_GET['saved'] ) ) : ?>
			<div class="notice notice-success is-dismissible"><p>تم الحفظ. ستظهر التغييرات في الموقع خلال دقيقة تقريبًا.</p></div>
		<?php endif; ?>
		<p>هذه الأرقام تظهر للجميع في صفحة التبرع. <strong>راجعها بعناية قبل الحفظ.</strong> اترك الصف فارغًا لإخفائه.</p>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
			<input type="hidden" name="action" value="ibcms_save_donation">
			<?php wp_nonce_field( 'ibcms_save_donation' ); ?>
			<table class="widefat striped" style="max-width:900px">
				<thead><tr><th>الاسم بالعربية</th><th>Name (English)</th><th>الرقم</th></tr></thead>
				<tbody>
				<?php foreach ( $methods as $i => $row ) : ?>
					<tr>
						<td><input type="text" class="regular-text" style="width:100%" name="m_ar[<?php echo (int) $i; ?>]" value="<?php echo esc_attr( $row['ar'] ); ?>"></td>
						<td><input type="text" class="regular-text" style="width:100%;direction:ltr" name="m_en[<?php echo (int) $i; ?>]" value="<?php echo esc_attr( $row['en'] ); ?>"></td>
						<td><input type="text" class="regular-text" style="width:100%;direction:ltr" name="m_num[<?php echo (int) $i; ?>]" value="<?php echo esc_attr( $row['number'] ); ?>"></td>
					</tr>
				<?php endforeach; ?>
				</tbody>
			</table>
			<h2>الملاحظة تحت الأرقام</h2>
			<p><label>بالعربية<br><textarea name="note_ar" rows="3" style="width:100%;max-width:900px"><?php echo esc_textarea( $d['note_ar'] ); ?></textarea></label></p>
			<p><label>English<br><textarea name="note_en" rows="3" style="width:100%;max-width:900px;direction:ltr"><?php echo esc_textarea( $d['note_en'] ); ?></textarea></label></p>
			<?php submit_button( 'حفظ' ); ?>
		</form>
	</div>
	<?php
}

add_action( 'admin_post_ibcms_save_donation', function () {
	if ( ! current_user_can( 'ibcms_edit_donation' ) ) {
		wp_die( 'غير مسموح.', 403 );
	}
	check_admin_referer( 'ibcms_save_donation' );
	$ar  = isset( $_POST['m_ar'] ) ? (array) wp_unslash( $_POST['m_ar'] ) : array();
	$en  = isset( $_POST['m_en'] ) ? (array) wp_unslash( $_POST['m_en'] ) : array();
	$num = isset( $_POST['m_num'] ) ? (array) wp_unslash( $_POST['m_num'] ) : array();
	$methods = array();
	for ( $i = 0; $i < 10; $i++ ) {
		$a = isset( $ar[ $i ] ) ? sanitize_text_field( $ar[ $i ] ) : '';
		$e = isset( $en[ $i ] ) ? sanitize_text_field( $en[ $i ] ) : '';
		$n = isset( $num[ $i ] ) ? sanitize_text_field( $num[ $i ] ) : '';
		if ( '' === $n ) {
			continue;
		}
		$methods[] = array( 'ar' => $a, 'en' => '' !== $e ? $e : $a, 'number' => $n );
	}
	update_option( 'ib_donation', array(
		'methods' => $methods,
		'note_ar' => isset( $_POST['note_ar'] ) ? sanitize_textarea_field( wp_unslash( $_POST['note_ar'] ) ) : '',
		'note_en' => isset( $_POST['note_en'] ) ? sanitize_textarea_field( wp_unslash( $_POST['note_en'] ) ) : '',
	), false );
	wp_safe_redirect( admin_url( 'admin.php?page=ibcms-donation&saved=1' ) );
	exit;
} );

/* ------------------------------------------------------------------
 * الدور والصلاحيات
 * ------------------------------------------------------------------ */

function ibcms_cpt_caps() {
	$caps = array();
	foreach ( array( 'ibnews', 'ibactivity' ) as $s ) {
		$p = $s . '_items';
		foreach ( array(
			"edit_$s", "read_$s", "delete_$s",
			"edit_$p", "edit_others_$p", "publish_$p", "read_private_$p",
			"delete_$p", "delete_private_$p", "delete_published_$p", "delete_others_$p",
			"edit_private_$p", "edit_published_$p",
		) as $c ) {
			$caps[] = $c;
		}
	}
	return $caps;
}

function ibcms_activate() {
	$caps = array( 'read' => true, 'upload_files' => true );
	foreach ( ibcms_cpt_caps() as $c ) {
		$caps[ $c ] = true;
	}
	remove_role( 'ib_publisher' );
	add_role( 'ib_publisher', 'ناشر المحتوى', $caps );
	$admin = get_role( 'administrator' );
	if ( $admin ) {
		foreach ( ibcms_cpt_caps() as $c ) {
			$admin->add_cap( $c );
		}
		$admin->add_cap( 'ibcms_edit_donation' );
	}
	if ( false === get_option( 'ib_donation', false ) ) {
		add_option( 'ib_donation', ibcms_donation_defaults(), '', 'no' );
	}
	ibcms_seed_activities();
}
register_activation_hook( __FILE__, 'ibcms_activate' );

/** عند تحديث الإضافة من ملف جديد، تأكد من وجود الصلاحيات. */
add_action( 'admin_init', function () {
	if ( get_option( 'ibcms_version' ) !== IBCMS_VERSION ) {
		ibcms_activate();
		update_option( 'ibcms_version', IBCMS_VERSION, false );
	}
} );

function ibcms_is_publisher( $user = null ) {
	$user = $user ? $user : wp_get_current_user();
	return $user && $user->exists() && in_array( 'ib_publisher', (array) $user->roles, true ) && ! in_array( 'administrator', (array) $user->roles, true );
}

/* ------------------------------------------------------------------
 * تبسيط لوحة التحكم للناشر
 * ------------------------------------------------------------------ */

add_action( 'admin_menu', function () {
	if ( ! ibcms_is_publisher() ) {
		return;
	}
	global $menu;
	$keep = array( 'edit.php?post_type=ib_news', 'edit.php?post_type=ib_activity', 'upload.php', 'profile.php' );
	foreach ( (array) $menu as $item ) {
		if ( isset( $item[2] ) && ! in_array( $item[2], $keep, true ) ) {
			remove_menu_page( $item[2] );
		}
	}
}, 9999 );

add_action( 'admin_init', function () {
	if ( ! ibcms_is_publisher() ) {
		return;
	}
	global $pagenow;
	// منع فتح اللوحة الرئيسية وصفحات الأدوات
	if ( in_array( $pagenow, array( 'index.php', 'tools.php', 'options-general.php', 'plugins.php', 'themes.php', 'users.php', 'edit-comments.php' ), true ) && ! wp_doing_ajax() ) {
		wp_safe_redirect( admin_url( 'edit.php?post_type=ib_news' ) );
		exit;
	}
	remove_all_actions( 'admin_notices' );
	remove_all_actions( 'all_admin_notices' );
	add_filter( 'screen_options_show_screen', '__return_false' );
} );

add_filter( 'login_redirect', function ( $to, $req, $user ) {
	if ( $user instanceof WP_User && ibcms_is_publisher( $user ) ) {
		return admin_url( 'edit.php?post_type=ib_news' );
	}
	return $to;
}, 10, 3 );

add_action( 'admin_bar_menu', function ( $bar ) {
	if ( ! ibcms_is_publisher() ) {
		return;
	}
	foreach ( array( 'wp-logo', 'comments', 'new-content', 'updates', 'site-name', 'customize', 'search' ) as $id ) {
		$bar->remove_node( $id );
	}
}, 999 );

add_action( 'admin_head', function () {
	if ( ! ibcms_is_publisher() ) {
		return;
	}
	?>
	<style>
		#wpfooter,#contextual-help-link-wrap,#screen-options-link-wrap,.update-nag,#wp-admin-bar-wp-logo{display:none!important}
		#minor-publishing-actions,#misc-publishing-actions .misc-pub-visibility,#misc-publishing-actions .misc-pub-post-status a.edit-post-status{display:none}
		#adminmenu li.wp-menu-separator{display:none}
	</style>
	<?php
} );

add_filter( 'admin_footer_text', '__return_empty_string' );
add_filter( 'update_footer', '__return_empty_string', 99 );

/* ------------------------------------------------------------------
 * واجهة القراءة العامة (REST)
 * ------------------------------------------------------------------ */

function ibcms_str( $v ) {
	return is_string( $v ) ? $v : '';
}

function ibcms_image( $post_id ) {
	$tid = get_post_thumbnail_id( $post_id );
	if ( ! $tid ) {
		return null;
	}
	$url = wp_get_attachment_image_url( $tid, 'large' );
	if ( ! $url ) {
		return null;
	}
	return array(
		'url' => esc_url_raw( $url ),
		'alt' => ibcms_str( get_post_meta( $tid, '_wp_attachment_image_alt', true ) ),
	);
}

function ibcms_news_item( $p ) {
	return array(
		'id'    => (int) $p->ID,
		'date'  => get_post_time( 'c', true, $p ),
		'title' => array( 'ar' => get_the_title( $p ), 'en' => ibcms_str( get_post_meta( $p->ID, '_ib_title_en', true ) ) ),
		'text'  => array( 'ar' => ibcms_str( get_post_meta( $p->ID, '_ib_text_ar', true ) ), 'en' => ibcms_str( get_post_meta( $p->ID, '_ib_text_en', true ) ) ),
		'image' => ibcms_image( $p->ID ),
		'link'  => ibcms_str( get_post_meta( $p->ID, '_ib_link', true ) ),
	);
}

function ibcms_activity_item( $p ) {
	return array(
		'id'       => (int) $p->ID,
		'slug'     => $p->post_name,
		'title'    => array( 'ar' => get_the_title( $p ), 'en' => ibcms_str( get_post_meta( $p->ID, '_ib_title_en', true ) ) ),
		'text'     => array( 'ar' => ibcms_str( get_post_meta( $p->ID, '_ib_text_ar', true ) ), 'en' => ibcms_str( get_post_meta( $p->ID, '_ib_text_en', true ) ) ),
		'image'    => ibcms_image( $p->ID ),
		'icon'     => ibcms_str( get_post_meta( $p->ID, '_ib_icon', true ) ),
		'order'    => (int) get_post_meta( $p->ID, '_ib_order', true ),
		'featured' => '1' === get_post_meta( $p->ID, '_ib_featured', true ),
		'group'    => ( $g = ibcms_str( get_post_meta( $p->ID, '_ib_group', true ) ) ) && array_key_exists( $g, ibcms_groups() ) ? $g : 'general',
	);
}

add_action( 'rest_api_init', function () {
	register_rest_route( IBCMS_NS, '/news', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'args'                => array(
			'per_page' => array( 'default' => 12, 'sanitize_callback' => 'absint' ),
			'page'     => array( 'default' => 1, 'sanitize_callback' => 'absint' ),
		),
		'callback'            => function ( WP_REST_Request $r ) {
			$per = max( 1, min( 50, (int) $r['per_page'] ) );
			$pg  = max( 1, (int) $r['page'] );
			$q   = new WP_Query( array(
				'post_type'      => 'ib_news',
				'post_status'    => 'publish',
				'posts_per_page' => $per,
				'paged'          => $pg,
				'orderby'        => 'date',
				'order'          => 'DESC',
				'no_found_rows'  => false,
			) );
			return array(
				'items' => array_map( 'ibcms_news_item', $q->posts ),
				'total' => (int) $q->found_posts,
				'pages' => (int) $q->max_num_pages,
			);
		},
	) );

	register_rest_route( IBCMS_NS, '/news/(?P<id>\d+)', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $r ) {
			$p = get_post( (int) $r['id'] );
			if ( ! $p || 'ib_news' !== $p->post_type || 'publish' !== $p->post_status ) {
				return new WP_Error( 'ib_not_found', 'غير موجود', array( 'status' => 404 ) );
			}
			return ibcms_news_item( $p );
		},
	) );

	register_rest_route( IBCMS_NS, '/activities', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			$q = new WP_Query( array(
				'post_type'      => 'ib_activity',
				'post_status'    => 'publish',
				'posts_per_page' => 100,
				'meta_key'       => '_ib_order',
				'orderby'        => array( 'meta_value_num' => 'ASC', 'date' => 'ASC' ),
				'no_found_rows'  => true,
			) );
			return array( 'items' => array_map( 'ibcms_activity_item', $q->posts ) );
		},
	) );

	register_rest_route( IBCMS_NS, '/donation', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			$d = ibcms_get_donation();
			$m = array();
			foreach ( $d['methods'] as $row ) {
				$m[] = array(
					'label'  => array( 'ar' => ibcms_str( $row['ar'] ), 'en' => ibcms_str( $row['en'] ) ),
					'number' => ibcms_str( $row['number'] ),
				);
			}
			return array(
				'methods' => $m,
				'note'    => array( 'ar' => ibcms_str( $d['note_ar'] ), 'en' => ibcms_str( $d['note_en'] ) ),
			);
		},
	) );
} );

/** سياسة CORS صارمة لواجهتنا فقط، وتخزين مؤقت قصير. */
add_filter( 'rest_pre_serve_request', function ( $served, $result, $request ) {
	if ( 0 !== strpos( $request->get_route(), '/' . IBCMS_NS . '/' ) ) {
		return $served;
	}
	remove_filter( 'rest_pre_serve_request', 'rest_send_cors_headers' );
	header( 'Vary: Origin', false );
	$origin = isset( $_SERVER['HTTP_ORIGIN'] ) ? esc_url_raw( wp_unslash( $_SERVER['HTTP_ORIGIN'] ) ) : '';
	if ( $origin && in_array( untrailingslashit( $origin ), ibcms_allowed_origins(), true ) ) {
		header( 'Access-Control-Allow-Origin: ' . untrailingslashit( $origin ) );
		header( 'Access-Control-Allow-Methods: GET, OPTIONS' );
	}
	header( 'Cache-Control: public, max-age=60' );
	header( 'X-Content-Type-Options: nosniff' );
	return $served;
}, 0, 3 );

/* ------------------------------------------------------------------
 * تقوية بسيطة
 * ------------------------------------------------------------------ */

// منع كشف أسماء المستخدمين لغير المسجلين
add_filter( 'rest_endpoints', function ( $endpoints ) {
	if ( ! is_user_logged_in() ) {
		foreach ( array_keys( $endpoints ) as $route ) {
			if ( 0 === strpos( $route, '/wp/v2/users' ) ) {
				unset( $endpoints[ $route ] );
			}
		}
	}
	return $endpoints;
} );
add_filter( 'xmlrpc_enabled', '__return_false' );
remove_action( 'wp_head', 'wp_generator' );
add_filter( 'the_generator', '__return_empty_string' );

/* ------------------------------------------------------------------
 * أنشطة افتراضية (تُضاف مرة واحدة لكل نشاط، ولا يعاد إنشاء ما يحذفه المدير)
 * ------------------------------------------------------------------ */

function ibcms_default_activities() {
	// slug, order, icon, featured, group, title_ar, title_en, text_ar, text_en
	return array(
		array( 'renovation', 10, '', 1, 'general', 'مهمة بناء (ترميم المنازل)', 'Building Mission (home renovation)',
			'بفضل جهود المتطوعين وتكاتف الأيادي الخيرة، نرمم المنازل المتضررة ونوفر سقفًا آمنًا وبيئة مناسبة للعائلات المتعففة.',
			'Thanks to the efforts of volunteers and generous hands, we renovate damaged homes and provide a safe roof and a suitable environment for families in need.' ),
		array( 'food', 20, '', 1, 'general', 'سلال غذائية', 'Food baskets',
			'بدعم من فريق بناة العراق التطوعي نوزع سلالًا غذائية على الأسر المحتاجة.',
			'With the support of the Iraq Builders volunteer team, we distribute food baskets to families in need.' ),
		array( 'education', 30, '', 1, 'general', 'حقيبة مدرسية', 'School bags',
			'حقائب مدرسية مجهزة بالكامل للطلاب المحتاجين، ضمن مبادرة الفريق لدعم التعليم.',
			'Fully equipped school bags for students in need, as part of the team\'s initiative to support education.' ),
		array( 'appliances', 40, '', 1, 'general', 'أجهزة كهربائية ومنزلية', 'Electrical and home appliances',
			'نوزع الأجهزة الكهربائية والمنزلية الضرورية للأسر ذات الدخل المحدود، لتحسين جودة الحياة اليومية وتخفيف الأعباء المالية.',
			'We distribute essential electrical and household appliances to low-income families, improving daily life and easing financial burdens.' ),
		array( 'medical-care', 50, 'cross', 0, 'general', 'رعاية طبية', 'Medical care',
			'عمليات وأدوية: تغطية تكاليف العمليات الجراحية والدواء للمحتاجين.',
			'Surgeries and medicines: covering the cost of surgical operations and medicine for those in need.' ),
		array( 'eid-clothing', 60, 'shirt', 0, 'general', 'كسوة العيد', 'Eid clothing',
			'ملابس جديدة للأطفال والعائلات في أعياد الفطر والأضحى.',
			'New clothes for children and families at Eid al-Fitr and Eid al-Adha.' ),
		array( 'livelihood', 70, 'tools', 0, 'general', 'مشاريع تشغيلية', 'Livelihood projects',
			'تعزيز الاستقلالية الاقتصادية للأفراد بتوفير فرص عمل ومشاريع صغيرة.',
			'Strengthening individuals\' economic independence through jobs and small projects.' ),
		array( 'sponsorship', 80, 'heart', 0, 'general', 'كفالات', 'Sponsorships',
			'أنشطة كفالة طبية ودراسية ومعيشية للأسر والأفراد المحتاجين.',
			'Medical, educational and living sponsorship activities for families and individuals in need.' ),
		array( 'financial-aid', 90, 'gift', 0, 'general', 'مساعدات مالية', 'Financial aid',
			'مساعدات مالية للأسر والأفراد الذين يواجهون صعوبات اقتصادية.',
			'Financial assistance for families and individuals facing economic hardship.' ),
		array( 'khatwa', 100, '', 0, 'project', 'مشروع خطوة', 'Khatwa project',
			'مشروع يمكّن الشباب والباحثين عن العمل عبر تطوير مهاراتهم المهنية ودمجهم في سوق العمل. يسعى المشروع إلى سد الفجوة بين المهارات التي يمتلكها الباحثون عن العمل واحتياجات السوق، وتدريب الأفراد على مهارات مهنية متخصصة.',
			'A project that empowers young people and job seekers by developing their professional skills and integrating them into the labor market. It aims to bridge the gap between job seekers\' skills and market needs, and to train individuals in specialized professional skills.' ),
		array( 'ramadan-iftar', 110, 'moon', 0, 'ramadan', 'إفطار العوائل', 'Family iftars',
			'موائد إفطار للعائلات المحتاجة.', 'Iftar tables for families in need.' ),
		array( 'zakat-fitr', 120, 'heart', 0, 'ramadan', 'زكاة الفطرة', 'Zakat al-Fitr',
			'نوصل زكاة الفطرة لمستحقيها.', 'Delivering Zakat al-Fitr to those who deserve it.' ),
		array( 'ramadan-baskets', 130, 'gift', 0, 'ramadan', 'سلات رمضانية', 'Ramadan baskets',
			'سلات غذائية خاصة بالشهر الفضيل.', 'Food baskets for the holy month.' ),
		array( 'ramadan-eid-clothing', 140, 'shirt', 0, 'ramadan', 'كسوة العيد', 'Eid clothing',
			'فرحة العيد بملابس جديدة للأطفال.', 'The joy of Eid with new clothes for children.' ),
	);
}

function ibcms_seed_activities() {
	$seeded = get_option( 'ibcms_seeded_slugs', array() );
	if ( ! is_array( $seeded ) ) {
		$seeded = array();
	}
	foreach ( ibcms_default_activities() as $it ) {
		if ( in_array( $it[0], $seeded, true ) ) {
			continue;
		}
		$seeded[] = $it[0];
		$exists   = get_posts( array( 'post_type' => 'ib_activity', 'name' => $it[0], 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids' ) );
		if ( $exists ) {
			continue;
		}
		$id = wp_insert_post( array(
			'post_type'   => 'ib_activity',
			'post_status' => 'publish',
			'post_title'  => $it[5],
			'post_name'   => $it[0],
		) );
		if ( $id && ! is_wp_error( $id ) ) {
			update_post_meta( $id, '_ib_order', $it[1] );
			update_post_meta( $id, '_ib_icon', $it[2] );
			update_post_meta( $id, '_ib_featured', $it[3] ? '1' : '0' );
			update_post_meta( $id, '_ib_group', $it[4] );
			update_post_meta( $id, '_ib_title_en', $it[6] );
			update_post_meta( $id, '_ib_text_ar', $it[7] );
			update_post_meta( $id, '_ib_text_en', $it[8] );
		}
	}
	update_option( 'ibcms_seeded_slugs', $seeded, false );
}
