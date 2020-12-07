package repositories.product;

import entities.ProductHistoryEntity;

import java.util.UUID;

public interface IProductHistoryRepository {
    void add(ProductHistoryEntity productHistoryEntity);
    ProductHistoryEntity getById(UUID id);
}
