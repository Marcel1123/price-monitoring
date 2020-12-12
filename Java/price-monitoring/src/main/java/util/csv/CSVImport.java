package util.csv;

import com.opencsv.CSVReader;
import entities.CityEntity;
import entities.LocationEntity;
import entities.ProductEntity;
import entities.ProductHistoryEntity;
import lombok.SneakyThrows;
import repositories.city.CityRepository;
import repositories.location.LocationRepository;
import repositories.product.ProductHistoryRepository;
import repositories.product.ProductRepository;
import util.enums.Currency;
import util.enums.FurnishType;
import util.enums.ProductType;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import java.io.FileReader;
import java.sql.Date;
import java.util.LinkedList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Named
@ApplicationScoped
public class CSVImport {
    @Inject
    private LocationRepository locationRepository;
    @Inject
    private CityRepository cityRepository;
    @Inject
    private ProductHistoryRepository productHistoryRepository;
    @Inject
    private ProductRepository productRepository;

    @SneakyThrows
    public void importLocationFromCSV(String csvLocation){

        CSVReader csvReader = new CSVReader(new FileReader(csvLocation));

        String[] line = null;
        line = csvReader.readNext();
        while ((line = csvReader.readNext()) != null) {
            LocationEntity locationEntity = new LocationEntity();
            locationEntity.setCity(cityRepository.getById(UUID.fromString(line[2])));
            locationEntity.setId(UUID.fromString(line[1]));
            locationEntity.setAddress(line[0]);

            locationRepository.add(locationEntity);
        }

        csvReader.close();
    }

    @SneakyThrows
    public void importCityFromCSV(String csvLocation){
        CSVReader csvReader = new CSVReader(new FileReader(csvLocation));

        String[] line = null;
        while ((line = csvReader.readNext()) != null) {
            try {
                if(cityRepository.getById(UUID.fromString(line[0])) == null){
                    CityEntity cityEntity = new CityEntity();
                    cityEntity.setId(UUID.fromString(line[0]));
                    cityEntity.setName(line[1]);
                    cityEntity.setCountry(line[2]);

                    cityRepository.addCity(cityEntity);
                }
            } catch (Exception e){

            }
        }
    }

    @SneakyThrows
    public void importProductFromCSV(String csvLocationProduct, String csvLocationHistory){
        CSVReader csvReader = new CSVReader(new FileReader(csvLocationHistory));
        CSVReader csvReaderProduct = new CSVReader(new FileReader(csvLocationProduct));

        List<ProductEntity> products = new LinkedList<>();

        List<String[]> productHistory = csvReader.readAll();
        List<String[]> productCSV = csvReaderProduct.readAll();

        for(String[] product : productCSV){
            try{
                ProductEntity productEntity = new ProductEntity();
                productEntity.setId(UUID.fromString(product[0]));
                productEntity.setSize(Double.parseDouble(product[1]));
                productEntity.setLocation(locationRepository.getById(UUID.fromString(product[2])));
                productEntity.setType(ProductType.valueOf(product[3]));
                productEntity.setFurnishType(FurnishType.valueOf(product[4]));
                try{
                    productEntity.setFloorNumber(Integer.parseInt(product[5]));
                } catch (NumberFormatException e){
                    productEntity.setFloorNumber(Integer.MIN_VALUE);
                }
                try{
                    productEntity.setNumberOfFloors(Integer.parseInt(product[6]));
                } catch (NumberFormatException e){
                    productEntity.setNumberOfFloors(Integer.MIN_VALUE);
                }
                try{
                    productEntity.setYearOfConstruction(Integer.parseInt(product[7]));
                } catch (NumberFormatException e){
                    productEntity.setYearOfConstruction(Integer.MIN_VALUE);
                }
                productEntity.setNumberOfRooms(Integer.parseInt(product[8]));

                productEntity.setHistory(new LinkedList<>());
                productEntity.setPrediction(new LinkedList<>());

                List<String[]> history = productHistory.stream()
                        .filter(obj -> obj[1].equals(product[0]))
                        .collect(Collectors.toList());

                for(String[] h : history){
                    try{
                        ProductHistoryEntity productHistoryEntity = new ProductHistoryEntity();
                        productHistoryEntity.setId(UUID.fromString(h[0]));
                        productHistoryEntity.setCurrency(Currency.valueOf(h[4]));
                        productHistoryEntity.setPrice(Double.parseDouble(h[3]));
                        productHistoryEntity.setDate(Date.valueOf(h[2]));

                        productEntity.getHistory().add(productHistoryEntity);
                    } catch (Exception e){

                    }
                }
                productRepository.add(productEntity);
            } catch (Exception e){

            }
        }
    }

    public void startImport(String path){
        importCityFromCSV(path + "/city.csv");
        importLocationFromCSV(path + "/locations.csv");
        importProductFromCSV(path + "/products.csv", path + "/history.csv");
    }
}
