package repositories.location;

import entities.CityEntity;
import entities.LocationEntity;

import java.util.List;
import java.util.UUID;

public interface ILocationRepository {
    List<LocationEntity> getAll();
    void add(LocationEntity locationEntity);
    LocationEntity getById(UUID id);
    List<LocationEntity> getDistinct();
    List<LocationEntity> getByAddress(String address);
    List<LocationEntity> getByCityId(UUID id);
}
