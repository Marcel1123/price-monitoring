package repositories.product;

import entities.ProductEntity;

import java.util.UUID;

public interface IProductRepository {
    void add(ProductEntity productEntity);
    ProductEntity getById(UUID id);
}
