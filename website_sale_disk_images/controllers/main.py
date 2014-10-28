# -*- coding: utf-8 -*-

import logging
import werkzeug

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website_sale_disk_images.models.product import get_gallery

logger = logging.getLogger(__name__)


class website_sale(http.Controller):
    @http.route(['/shop/product/image-disk/'], type='json', auth="public", methods=['POST'], website=True)
    def image_disk(self, product_id, sizes):
        """
        Añade un producto a la lista de deseos del usuario en el sitio web indicado
        """
        cr, uid, context, registry, website = request.cr, request.uid, request.context, request.registry, request.website

        try:
            product_id = int(product_id)
            list
        except:
            logger.exception(u"Error parseando parametros")
            raise werkzeug.exceptions.NotFound()

        # leemos los grupos del usuario
        show_path = request.registry['res.users'].has_group(cr, uid, 'base.group_website_publisher')

        # leemos el producto
        orm_product = registry.get('product.product')
        if len(orm_product.search(cr, uid, [('id', '=', product_id)])) == 0:
            raise werkzeug.exceptions.NotFound()
        product = orm_product.browse(cr, uid, product_id, context=context)
        logger.info("poducto {}".format(product.product_tmpl_id))

        # leemos la galeria
        g = get_gallery(product)

        # devolvemos images
        data = {'product': product.product_tmpl_id.name, 'images': []}
        if show_path:
            data['name'] = g.name_product
            data['path'] = g.path_product

        for image in g:
            data_image = {key: None for key in ['{}x{}'.format(w, h) for w, h in sizes] + ['original']}
            data_image['original'] = image.get()
            for w, h in sizes:
                data_image['{}x{}'.format(w, h)] = image.get(width=w, height=h)
            data['images'].append(data_image)

        return data